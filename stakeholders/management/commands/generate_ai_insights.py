from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from stakeholders.models import Stakeholder, Engagement
from ai_assistant.services import GeminiService
import random


class Command(BaseCommand):
    help = 'Generate AI insights for existing stakeholder data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            default='admin',
            help='Username to generate insights for (default: admin)',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limit number of stakeholders to process',
        )

    def handle(self, *args, **options):
        username = options['user']
        limit = options.get('limit')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist')
            )
            return

        gemini_service = GeminiService()
        
        if not gemini_service.is_available():
            self.stdout.write(
                self.style.WARNING(
                    'Gemini AI service is not available. Please configure GEMINI_API_KEY in settings.'
                )
            )
            # Generate mock AI insights instead
            self.generate_mock_insights(user, limit)
            return

        stakeholders = Stakeholder.objects.filter(created_by=user)
        if limit:
            stakeholders = stakeholders[:limit]

        self.stdout.write(f"Generating AI insights for {stakeholders.count()} stakeholders...")

        for stakeholder in stakeholders:
            self.stdout.write(f"Processing: {stakeholder.name}")
            
            # Generate stakeholder insights
            if not stakeholder.ai_generated_insights:
                basic_info = {
                    'name': stakeholder.name,
                    'title': stakeholder.title,
                    'organization': stakeholder.organization,
                    'department': stakeholder.department,
                    'category': stakeholder.category,
                    'influence': stakeholder.influence,
                    'interest': stakeholder.interest,
                    'description': stakeholder.description,
                }
                
                insights = gemini_service.generate_stakeholder_profile(basic_info)
                stakeholder.ai_generated_insights = insights
                stakeholder.save()
                self.stdout.write(f"  Generated stakeholder insights")

            # Generate AI summaries for completed engagements
            completed_engagements = stakeholder.engagements.filter(
                status='completed',
                ai_summary=''
            )
            
            for engagement in completed_engagements:
                # Create mock meeting notes for AI analysis
                mock_notes = self.generate_mock_meeting_notes(engagement, stakeholder)
                
                stakeholder_info = {
                    'name': stakeholder.name,
                    'title': stakeholder.title,
                    'organization': stakeholder.organization,
                }
                
                summary_data = gemini_service.summarize_meeting(mock_notes, stakeholder_info)
                
                if isinstance(summary_data, dict):
                    engagement.ai_summary = summary_data.get('summary', '')
                    engagement.ai_action_items = summary_data.get('action_items', '')
                    engagement.ai_sentiment_analysis = summary_data.get('sentiment', '')
                    engagement.save()
                    self.stdout.write(f"  Generated AI summary for: {engagement.title}")

        self.stdout.write(
            self.style.SUCCESS('Successfully generated AI insights for all stakeholders')
        )

    def generate_mock_insights(self, user, limit):
        """Generate mock AI insights when Gemini service is not available"""
        stakeholders = Stakeholder.objects.filter(created_by=user)
        if limit:
            stakeholders = stakeholders[:limit]

        mock_insights_templates = {
            'very_high': [
                "This stakeholder holds significant decision-making authority and should be engaged regularly with strategic-level communications. Their high influence requires careful relationship management and proactive updates on major initiatives. Consider scheduling regular executive briefings and ensuring they have early visibility into important decisions.",
                "As a key decision maker, this stakeholder's support is crucial for project success. They likely prefer high-level summaries with clear business impact and ROI metrics. Engagement should focus on strategic alignment and long-term value proposition. Regular face-to-face meetings are recommended.",
            ],
            'high': [
                "This stakeholder has substantial influence within their domain and can significantly impact project outcomes. They should be kept informed of major developments and consulted on decisions that affect their area of responsibility. Regular communication and relationship building are important.",
                "Strong influencer who can serve as a project champion or create obstacles if not properly engaged. Focus on building trust through consistent communication and demonstrating value. They may appreciate being involved in strategic planning discussions.",
            ],
            'medium': [
                "This stakeholder has moderate influence and should be engaged through regular updates and targeted communications. They may have valuable insights and can help with implementation. Consider involving them in working groups or advisory capacities.",
                "Steady contributor who can provide valuable input and support. Engagement should be consistent but not overwhelming. They likely appreciate being kept informed and having opportunities to provide feedback on relevant initiatives.",
            ],
            'low': [
                "While having lower direct influence, this stakeholder may represent important perspectives or constituencies. Keep them informed through standard communication channels and be responsive to their concerns. They may have valuable insights on implementation impacts.",
                "Limited direct influence but may have important connections or represent key user groups. Maintain positive relationships through inclusive communication and consider their feedback on user experience and practical implementation aspects.",
            ]
        }

        for stakeholder in stakeholders:
            if not stakeholder.ai_generated_insights:
                templates = mock_insights_templates.get(stakeholder.influence, mock_insights_templates['medium'])
                insight = random.choice(templates)
                
                # Add category-specific insights
                category_additions = {
                    'customer': " As a customer stakeholder, their satisfaction directly impacts business success. Focus on value delivery and addressing their specific needs and concerns.",
                    'investor': " As an investor, they are primarily concerned with returns and growth metrics. Communications should emphasize business value, market opportunity, and risk management.",
                    'regulator': " As a regulatory stakeholder, ensure all compliance requirements are met and maintain transparent communication about adherence to relevant standards and regulations.",
                    'supplier': " As a supplier stakeholder, focus on partnership benefits, integration efficiency, and mutual value creation opportunities.",
                }
                
                if stakeholder.category in category_additions:
                    insight += category_additions[stakeholder.category]
                
                stakeholder.ai_generated_insights = insight
                stakeholder.save()
                self.stdout.write(f"Generated mock insights for: {stakeholder.name}")

        # Generate mock AI summaries for completed engagements
        completed_engagements = Engagement.objects.filter(
            stakeholder__created_by=user,
            status='completed',
            ai_summary=''
        )
        
        if limit:
            completed_engagements = completed_engagements[:limit * 2]  # Roughly 2 per stakeholder

        mock_summaries = [
            "Productive discussion covering key project milestones and stakeholder expectations. Strong alignment achieved on next steps and timeline.",
            "Comprehensive review of current status with positive feedback on team performance. Several action items identified for follow-up.",
            "Strategic planning session with good participation and valuable insights shared. Stakeholder expressed satisfaction with progress.",
            "Regular check-in meeting covering operational updates and upcoming deliverables. No major concerns raised.",
            "Detailed technical discussion with stakeholder questions addressed satisfactorily. Additional documentation requested.",
        ]

        mock_action_items = [
            "• Follow up with technical team on implementation details\n• Schedule next review meeting within 2 weeks\n• Prepare updated project timeline",
            "• Share updated documentation with stakeholder\n• Coordinate with relevant teams on resource allocation\n• Set up follow-up call to address remaining questions",
            "• Prepare executive summary for senior leadership\n• Update project risk register\n• Schedule stakeholder feedback session",
            "• Continue with planned activities\n• Monitor progress against established milestones\n• Provide weekly status updates",
            "• Research additional requirements\n• Prepare technical specifications document\n• Arrange training session for end users",
        ]

        for engagement in completed_engagements:
            engagement.ai_summary = random.choice(mock_summaries)
            engagement.ai_action_items = random.choice(mock_action_items)
            engagement.ai_sentiment_analysis = engagement.sentiment or 'neutral'
            engagement.save()
            self.stdout.write(f"Generated mock AI summary for: {engagement.title}")

        self.stdout.write(
            self.style.SUCCESS('Successfully generated mock AI insights (Gemini service not available)')
        )

    def generate_mock_meeting_notes(self, engagement, stakeholder):
        """Generate realistic meeting notes for AI analysis"""
        notes_templates = {
            'meeting': f"""
Meeting with {stakeholder.name} - {engagement.title}

Attendees: Project team, {stakeholder.name}
Duration: {engagement.duration_minutes} minutes

Discussion Points:
- Reviewed current project status and milestones
- Discussed {stakeholder.name}'s requirements and expectations  
- Addressed questions about timeline and resource allocation
- Covered risk mitigation strategies and contingency planning

Key Outcomes:
{engagement.outcomes or 'Positive discussion with clear next steps identified.'}

Stakeholder Feedback:
- Generally satisfied with progress to date
- Raised some concerns about timeline pressure
- Requested more frequent status updates
- Emphasized importance of quality deliverables

Next Steps:
- Team to prepare detailed implementation plan
- Schedule follow-up meeting in 2 weeks
- Provide weekly status email updates
""",
            'email': f"""
Email exchange with {stakeholder.name} regarding {engagement.title}

Key topics covered:
- Project status update and current milestones
- Resource requirements and allocation
- Timeline adjustments and impact assessment
- Stakeholder concerns and feedback

Response from {stakeholder.name}:
{engagement.outcomes or 'Acknowledged update and provided constructive feedback.'}

Action items identified:
- Address specific concerns raised
- Provide additional documentation
- Schedule follow-up discussion if needed
""",
            'presentation': f"""
Presentation to {stakeholder.name} - {engagement.title}

Presentation covered:
- Current project status and achievements
- Key metrics and performance indicators
- Upcoming milestones and deliverables  
- Risk assessment and mitigation strategies

Stakeholder Questions & Feedback:
- Asked detailed questions about implementation approach
- Expressed interest in specific technical aspects
- Provided valuable insights from their perspective
- {engagement.outcomes or 'Overall positive reception with actionable feedback.'}

Follow-up actions:
- Address specific questions raised
- Provide additional technical details
- Schedule implementation review meeting
"""
        }
        
        template = notes_templates.get(engagement.type, notes_templates['meeting'])
        return template
