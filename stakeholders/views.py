from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.decorators.http import require_POST
from django.core.management import call_command
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import logout
import io
import sys

from .models import Stakeholder, Engagement, StakeholderRelationship, DemoSession
from .forms import StakeholderForm, EngagementForm
from ai_assistant.services import GeminiService

def welcome(request):
    """Welcome page for the application"""
    return render(request, 'welcome.html')

@login_required
def dashboard(request):
    """Main dashboard with stakeholder analytics"""
    user_stakeholders = Stakeholder.objects.filter(created_by=request.user)
    user_engagements = Engagement.objects.filter(created_by=request.user)
    
    # Analytics data
    total_stakeholders = user_stakeholders.count()
    total_engagements = user_engagements.count()
    
    # Calculate high priority stakeholders (priority score >= 12)
    high_priority_count = 0
    for stakeholder in user_stakeholders.all():
        influence_score = {
            'low': 1, 'medium': 2, 'high': 3, 'very_high': 4
        }.get(stakeholder.influence, 1)
        
        interest_score = {
            'low': 1, 'medium': 2, 'high': 3, 'very_high': 4
        }.get(stakeholder.interest, 1)
        
        priority_score = influence_score * interest_score
        if priority_score >= 12:
            high_priority_count += 1
      # Recent activity
    recent_stakeholders = user_stakeholders[:5]
      # Get all upcoming engagements for count (not limited to 5)
    upcoming_engagements_query = user_engagements.filter(
        scheduled_date__gte=timezone.now(),
        status='planned'
    )
    upcoming_engagements_count = upcoming_engagements_query.count()
    
    # Get overdue engagements (planned but past due)
    overdue_engagements_count = user_engagements.filter(
        scheduled_date__lt=timezone.now(),
        status='planned'
    ).count()
    
    # Get first 5 for display in recent activity
    upcoming_engagements = upcoming_engagements_query[:5]
    
    # Stakeholder distribution by influence/interest
    influence_data = user_stakeholders.values('influence').annotate(count=Count('influence'))
    interest_data = user_stakeholders.values('interest').annotate(count=Count('interest'))
    category_data = user_stakeholders.values('category').annotate(count=Count('category'))
    
    # Engagement metrics
    engagement_types = user_engagements.values('type').annotate(count=Count('type'))
      # Prepare stakeholder data for interactive grid
    stakeholders_json = []
    for stakeholder in user_stakeholders.all():
        # Convert influence/interest to numeric scores for positioning
        influence_score = {
            'low': 1, 'medium': 2, 'high': 3, 'very_high': 4
        }.get(stakeholder.influence, 1)
        
        interest_score = {
            'low': 1, 'medium': 2, 'high': 3, 'very_high': 4
        }.get(stakeholder.interest, 1)
        
        # Calculate priority score (max 16: 4*4)
        priority_score = influence_score * interest_score
        
        stakeholders_json.append({
            'id': stakeholder.id,
            'name': stakeholder.name,
            'title': stakeholder.title or 'N/A',
            'organization': stakeholder.organization or 'N/A',
            'influence': stakeholder.influence,
            'interest': stakeholder.interest,
            'influenceScore': influence_score,
            'interestScore': interest_score,
            'priorityScore': priority_score,
        })    
    # Check demo mode status
    try:
        demo_session = request.user.demo_session
        is_demo_mode = demo_session.is_demo_mode
        demo_scenario = demo_session.demo_scenario
    except DemoSession.DoesNotExist:
        is_demo_mode = False
        demo_scenario = None
    
    import json
    context = {
        'total_stakeholders': total_stakeholders,
        'overdue_engagements_count': overdue_engagements_count,
        'high_priority_count': high_priority_count,
        'upcoming_engagements_count': upcoming_engagements_count,
        'recent_stakeholders': recent_stakeholders,
        'upcoming_engagements': upcoming_engagements,
        'influence_data': json.dumps(list(influence_data)),
        'interest_data': json.dumps(list(interest_data)),
        'category_data': json.dumps(list(category_data)),
        'engagement_types': json.dumps(list(engagement_types)),
        'stakeholders_json': json.dumps(stakeholders_json),
        'is_demo_mode': is_demo_mode,
        'demo_scenario': demo_scenario,
    }
    
    return render(request, 'stakeholders/dashboard.html', context)

@login_required
def stakeholder_list(request):
    """List all stakeholders with search and filtering"""
    stakeholders = Stakeholder.objects.filter(created_by=request.user)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        stakeholders = stakeholders.filter(
            Q(name__icontains=search_query) |
            Q(organization__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(department__icontains=search_query)
        )
    
    # Filtering
    influence_filter = request.GET.get('influence', '')
    if influence_filter:
        stakeholders = stakeholders.filter(influence=influence_filter)
    
    category_filter = request.GET.get('category', '')
    if category_filter:
        stakeholders = stakeholders.filter(category=category_filter)
    
    # Priority filtering (high priority = priority score >= 12)
    priority_filter = request.GET.get('priority', '')
    if priority_filter == 'high':
        high_priority_ids = []
        for stakeholder in stakeholders:
            influence_score = {
                'low': 1, 'medium': 2, 'high': 3, 'very_high': 4
            }.get(stakeholder.influence, 1)
            
            interest_score = {
                'low': 1, 'medium': 2, 'high': 3, 'very_high': 4
            }.get(stakeholder.interest, 1)
            
            priority_score = influence_score * interest_score
            if priority_score >= 12:
                high_priority_ids.append(stakeholder.id)
        
        stakeholders = stakeholders.filter(id__in=high_priority_ids)
      # Pagination
    paginator = Paginator(stakeholders, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'influence_filter': influence_filter,
        'category_filter': category_filter,
        'priority_filter': priority_filter,
        'influence_choices': Stakeholder.INFLUENCE_CHOICES,
        'category_choices': Stakeholder.CATEGORY_CHOICES,
    }
    
    return render(request, 'stakeholders/stakeholder_list.html', context)

@login_required
def stakeholder_detail(request, pk):
    """Detailed view of a stakeholder"""
    stakeholder = get_object_or_404(Stakeholder, pk=pk, created_by=request.user)
    
    # Smart ordering for engagements: show upcoming first, then recent past ones
    from django.db.models import Case, When, Value, IntegerField
    engagements = stakeholder.engagements.annotate(
        is_future=Case(
            When(scheduled_date__gte=timezone.now(), then=Value(0)),  # Future = 0 (first)
            default=Value(1),  # Past = 1 (second)
            output_field=IntegerField()
        )
    ).order_by('is_future', 'scheduled_date')[:10]  # Top 10 relevant engagements
    
    relationships = StakeholderRelationship.objects.filter(
        Q(from_stakeholder=stakeholder) | Q(to_stakeholder=stakeholder)
    )
    
    context = {
        'stakeholder': stakeholder,
        'engagements': engagements,
        'relationships': relationships,
    }
    
    return render(request, 'stakeholders/stakeholder_detail.html', context)

@login_required
def stakeholder_create(request):
    """Create new stakeholder"""
    if request.method == 'POST':
        form = StakeholderForm(request.POST)
        if form.is_valid():
            stakeholder = form.save(commit=False)
            stakeholder.created_by = request.user
            
            # AI Profile Enhancement
            if request.POST.get('generate_ai_insights'):
                gemini_service = GeminiService()
                basic_info = {
                    'name': stakeholder.name,
                    'title': stakeholder.title,
                    'organization': stakeholder.organization,
                    'department': stakeholder.department,
                    'category': stakeholder.category,
                }
                stakeholder.ai_generated_insights = gemini_service.generate_stakeholder_profile(basic_info)
            
            stakeholder.save()
            messages.success(request, f'Stakeholder "{stakeholder.name}" created successfully!')
            return redirect('stakeholder_detail', pk=stakeholder.pk)
    else:
        form = StakeholderForm()
    
    context = {
        'form': form,
        'title': 'Add New Stakeholder',
    }
    
    return render(request, 'stakeholders/stakeholder_form.html', context)

@login_required
def stakeholder_edit(request, pk):
    """Edit existing stakeholder"""
    stakeholder = get_object_or_404(Stakeholder, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = StakeholderForm(request.POST, instance=stakeholder)
        if form.is_valid():
            stakeholder = form.save()
            
            # Regenerate AI insights if requested
            if request.POST.get('regenerate_ai_insights'):
                gemini_service = GeminiService()
                basic_info = {
                    'name': stakeholder.name,
                    'title': stakeholder.title,
                    'organization': stakeholder.organization,
                    'department': stakeholder.department,
                    'category': stakeholder.category,
                }
                stakeholder.ai_generated_insights = gemini_service.generate_stakeholder_profile(basic_info)
                stakeholder.save()
            
            messages.success(request, f'Stakeholder "{stakeholder.name}" updated successfully!')
            return redirect('stakeholder_detail', pk=stakeholder.pk)
    else:
        form = StakeholderForm(instance=stakeholder)
    
    context = {
        'form': form,
        'stakeholder': stakeholder,
        'title': f'Edit {stakeholder.name}',
    }
    
    return render(request, 'stakeholders/stakeholder_form.html', context)

@login_required
def stakeholder_delete(request, pk):
    """Delete stakeholder"""
    stakeholder = get_object_or_404(Stakeholder, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        name = stakeholder.name
        stakeholder.delete()
        messages.success(request, f'Stakeholder "{name}" deleted successfully!')
        return redirect('stakeholder_list')
    
    context = {
        'stakeholder': stakeholder,
    }
    
    return render(request, 'stakeholders/stakeholder_confirm_delete.html', context)

@login_required
def engagement_list(request):
    """List all engagements"""
    engagements = Engagement.objects.filter(created_by=request.user)
      # Filtering
    status_filter = request.GET.get('status', '')
    if status_filter:
        engagements = engagements.filter(status=status_filter)
    
    stakeholder_filter = request.GET.get('stakeholder', '')
    if stakeholder_filter:
        engagements = engagements.filter(stakeholder_id=stakeholder_filter)
    
    # Filter by engagement type
    type_filter = request.GET.get('type', '')
    if type_filter:
        engagements = engagements.filter(type=type_filter)
      # Filter for upcoming meetings
    upcoming_filter = request.GET.get('upcoming', '')
    if upcoming_filter == 'true':
        engagements = engagements.filter(
            scheduled_date__gte=timezone.now(),
            status='planned'
        )
    
    # Filter for overdue engagements
    overdue_filter = request.GET.get('overdue', '')
    if overdue_filter == 'true':
        engagements = engagements.filter(
            scheduled_date__lt=timezone.now(),
            status='planned'
        )
    
    # Smart ordering: Show upcoming first (ascending), then past ones (descending)
    from django.db.models import Case, When, Value, IntegerField
    engagements = engagements.annotate(
        is_future=Case(
            When(scheduled_date__gte=timezone.now(), then=Value(0)),  # Future = 0 (first)
            default=Value(1),  # Past = 1 (second)
            output_field=IntegerField()
        )
    ).order_by('is_future', 'scheduled_date')
      # Pagination
    paginator = Paginator(engagements, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get stakeholders for filter dropdown
    user_stakeholders = Stakeholder.objects.filter(created_by=request.user)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'stakeholder_filter': stakeholder_filter,
        'type_filter': type_filter,
        'upcoming_filter': upcoming_filter,
        'overdue_filter': overdue_filter,
        'status_choices': Engagement.STATUS_CHOICES,
        'type_choices': Engagement.TYPE_CHOICES,
        'stakeholders': user_stakeholders,
    }
    
    return render(request, 'stakeholders/engagement_list.html', context)

@login_required
def engagement_create(request):
    """Create new engagement"""
    if request.method == 'POST':
        form = EngagementForm(request.POST, user=request.user)
        if form.is_valid():
            engagement = form.save(commit=False)
            engagement.created_by = request.user
            engagement.save()
            messages.success(request, f'Engagement "{engagement.title}" created successfully!')
            return redirect('engagement_detail', pk=engagement.pk)
    else:
        # Pre-select stakeholder if provided in URL
        stakeholder_id = request.GET.get('stakeholder')
        initial_data = {}
        if stakeholder_id:
            try:
                stakeholder = Stakeholder.objects.get(pk=stakeholder_id, created_by=request.user)
                initial_data['stakeholder'] = stakeholder
            except Stakeholder.DoesNotExist:
                pass
        
        form = EngagementForm(user=request.user, initial=initial_data)
    
    context = {
        'form': form,
        'title': 'Schedule New Engagement',
    }
    
    return render(request, 'stakeholders/engagement_form.html', context)

@login_required
def engagement_detail(request, pk):
    """Detailed view of an engagement"""
    engagement = get_object_or_404(Engagement, pk=pk, created_by=request.user)
    
    context = {
        'engagement': engagement,
    }
    
    return render(request, 'stakeholders/engagement_detail.html', context)

@login_required
def engagement_edit(request, pk):
    """Edit an existing engagement"""
    engagement = get_object_or_404(Engagement, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = EngagementForm(request.POST, instance=engagement, user=request.user)
        if form.is_valid():
            engagement = form.save()
            messages.success(request, f'Engagement "{engagement.title}" updated successfully!')
            return redirect('engagement_detail', pk=engagement.pk)
    else:
        form = EngagementForm(instance=engagement, user=request.user)
    
    context = {
        'form': form,
        'engagement': engagement,
        'title': f'Edit Engagement: {engagement.title}',
    }
    
    return render(request, 'stakeholders/engagement_form.html', context)

@login_required
@require_POST
def generate_ai_summary(request, engagement_pk):
    """Generate AI summary for an engagement"""
    engagement = get_object_or_404(Engagement, pk=engagement_pk, created_by=request.user)
    
    try:
        data = json.loads(request.body)
        meeting_notes = data.get('meeting_notes', '')
        
        if not meeting_notes:
            return JsonResponse({'error': 'No meeting notes provided'}, status=400)
        
        gemini_service = GeminiService()
        stakeholder_info = {
            'name': engagement.stakeholder.name,
            'title': engagement.stakeholder.title,
            'organization': engagement.stakeholder.organization,
        }
        
        summary_data = gemini_service.summarize_meeting(meeting_notes, stakeholder_info)
        
        # Update engagement with AI analysis
        engagement.ai_summary = summary_data.get('summary', '')
        engagement.ai_action_items = summary_data.get('action_items', '')
        engagement.ai_sentiment_analysis = summary_data.get('sentiment', '')
        engagement.save()
        
        return JsonResponse({
            'success': True,
            'summary': summary_data.get('summary', ''),
            'action_items': summary_data.get('action_items', ''),
            'sentiment': summary_data.get('sentiment', ''),
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def draft_communication(request):
    """Draft communication using AI"""
    try:
        data = json.loads(request.body)
        stakeholder_id = data.get('stakeholder_id')
        communication_type = data.get('communication_type', 'email')
        purpose = data.get('purpose', '')
        
        stakeholder = get_object_or_404(Stakeholder, pk=stakeholder_id, created_by=request.user)
        
        gemini_service = GeminiService()
        stakeholder_info = {
            'name': stakeholder.name,
            'title': stakeholder.title,
            'organization': stakeholder.organization,
            'influence': stakeholder.influence,
            'interest': stakeholder.interest,
            'category': stakeholder.category,
        }
        
        draft = gemini_service.draft_communication(stakeholder_info, communication_type, purpose)
        
        return JsonResponse({
            'success': True,
            'draft': draft,
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def api_stakeholders(request):
    """API endpoint to get stakeholders list for dropdowns"""
    try:
        stakeholders = Stakeholder.objects.filter(created_by=request.user).values(
            'id', 'name', 'title', 'organization'
        )
        
        return JsonResponse({
            'success': True,
            'stakeholders': list(stakeholders)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def meeting_summary(request):
    """Generate AI meeting summary"""
    try:
        data = json.loads(request.body)
        stakeholder_id = data.get('stakeholder_id')
        meeting_notes = data.get('meeting_notes', '')
        
        stakeholder = get_object_or_404(Stakeholder, pk=stakeholder_id, created_by=request.user)
        
        gemini_service = GeminiService()
        stakeholder_info = {
            'name': stakeholder.name,
            'title': stakeholder.title,
            'organization': stakeholder.organization,
            'influence': stakeholder.influence,
            'interest': stakeholder.interest,
            'category': stakeholder.category,
        }
        
        summary = gemini_service.summarize_meeting(meeting_notes, stakeholder_info)
        
        return JsonResponse({
            'success': True,
            'summary': summary,
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def load_demo_data(request):
    """Load demo data for the current user"""
    try:
        scenario = request.POST.get('scenario', 'standard')
        
        # Capture command output
        output = io.StringIO()
        call_command('load_demo_data', user=request.user.username, scenario=scenario, stdout=output)
        
        messages.success(request, f'Demo data loaded successfully! ({scenario.replace("_", " ").title()} scenario)')
        
        # Create or update demo session
        demo_session, created = DemoSession.objects.get_or_create(
            user=request.user,
            defaults={'demo_scenario': scenario}
        )
        demo_session.is_demo_mode = True
        demo_session.demo_scenario = scenario
        demo_session.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Demo data loaded successfully!',
            'scenario': scenario
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@require_POST
def clear_demo_data(request):
    """Clear all demo data for the current user"""
    try:
        # Count data before deletion
        stakeholder_count = Stakeholder.objects.filter(created_by=request.user).count()
        engagement_count = Engagement.objects.filter(created_by=request.user).count()
        relationship_count = StakeholderRelationship.objects.filter(created_by=request.user).count()
        
        # Clear data using management command
        output = io.StringIO()
        call_command('clear_demo_data', user=request.user.username, confirm=True, stdout=output)
        
        messages.success(
            request, 
            f'All data cleared successfully! Removed {stakeholder_count} stakeholders, '
            f'{engagement_count} engagements, and {relationship_count} relationships.'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Demo data cleared successfully!',
            'cleared': {
                'stakeholders': stakeholder_count,
                'engagements': engagement_count,
                'relationships': relationship_count
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def get_demo_status(request):
    """Get current demo mode status for the user"""
    try:
        demo_session = request.user.demo_session
        return JsonResponse({
            'is_demo_mode': demo_session.is_demo_mode,
            'demo_scenario': demo_session.demo_scenario,
            'demo_started_at': demo_session.demo_started_at.isoformat() if demo_session.demo_started_at else None
        })
    except DemoSession.DoesNotExist:
        return JsonResponse({
            'is_demo_mode': False,
            'demo_scenario': None,
            'demo_started_at': None
        })

def custom_logout(request):
    """Custom logout view that handles both GET and POST requests"""
    # Log out the user
    logout(request)
    # Render the logout template
    return render(request, 'auth/logout.html')
