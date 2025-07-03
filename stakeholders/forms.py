from django import forms
from django.contrib.auth.models import User
from .models import Stakeholder, Engagement, StakeholderRelationship

class StakeholderForm(forms.ModelForm):
    class Meta:
        model = Stakeholder
        fields = [
            'name', 'title', 'organization', 'department',
            'email', 'phone', 'influence', 'interest', 'category',
            'description', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'organization': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'influence': forms.Select(attrs={'class': 'form-select'}),
            'interest': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class EngagementForm(forms.ModelForm):
    class Meta:
        model = Engagement
        fields = [
            'stakeholder', 'title', 'type', 'status', 'scheduled_date',
            'duration_minutes', 'description', 'objectives', 'outcomes',
            'action_items', 'sentiment', 'effectiveness_rating'
        ]
        widgets = {
            'stakeholder': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'scheduled_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local', 'required': True}
            ),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'outcomes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'action_items': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sentiment': forms.Select(attrs={'class': 'form-select'}),
            'effectiveness_rating': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '1', 'max': '5'}
            ),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Only show stakeholders created by the current user
            self.fields['stakeholder'].queryset = Stakeholder.objects.filter(created_by=user)

class StakeholderRelationshipForm(forms.ModelForm):
    class Meta:
        model = StakeholderRelationship
        fields = ['from_stakeholder', 'to_stakeholder', 'relationship_type', 'description', 'strength']
        widgets = {
            'from_stakeholder': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'to_stakeholder': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'relationship_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'strength': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Only show stakeholders created by the current user
            stakeholders = Stakeholder.objects.filter(created_by=user)
            self.fields['from_stakeholder'].queryset = stakeholders
            self.fields['to_stakeholder'].queryset = stakeholders

class AIAssistantForm(forms.Form):
    """Form for AI assistant features"""
    stakeholder = forms.ModelChoiceField(
        queryset=Stakeholder.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select a stakeholder"
    )
    communication_type = forms.ChoiceField(
        choices=[
            ('email', 'Email'),
            ('letter', 'Formal Letter'),
            ('meeting_request', 'Meeting Request'),
            ('follow_up', 'Follow-up Message'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    purpose = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describe the purpose of this communication...'
        })
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['stakeholder'].queryset = Stakeholder.objects.filter(created_by=user)

class MeetingSummaryForm(forms.Form):
    """Form for AI meeting summary generation"""
    meeting_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Paste your meeting notes here...'
        }),
        help_text="Paste the raw meeting notes and AI will generate a structured summary"
    )
