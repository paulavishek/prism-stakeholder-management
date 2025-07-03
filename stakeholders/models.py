from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Stakeholder(models.Model):
    INFLUENCE_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High'),
    ]
    
    INTEREST_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High'),
    ]
    
    CATEGORY_CHOICES = [
        ('internal', 'Internal'),
        ('external', 'External'),
        ('customer', 'Customer'),
        ('supplier', 'Supplier'),
        ('investor', 'Investor'),
        ('regulator', 'Regulator'),
        ('community', 'Community'),
        ('media', 'Media'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=200, blank=True)
    
    # Contact Information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Stakeholder Analysis
    influence = models.CharField(max_length=20, choices=INFLUENCE_CHOICES, default='medium')
    interest = models.CharField(max_length=20, choices=INTEREST_CHOICES, default='medium')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='internal')
    
    # Additional Details
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    ai_generated_insights = models.TextField(blank=True, help_text="AI-generated insights about this stakeholder")
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stakeholders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.name} - {self.organization}"
    
    @property
    def influence_score(self):
        """Convert influence to numeric score for calculations"""
        scores = {'low': 1, 'medium': 2, 'high': 3, 'very_high': 4}
        return scores.get(self.influence, 2)
    
    @property
    def interest_score(self):
        """Convert interest to numeric score for calculations"""
        scores = {'low': 1, 'medium': 2, 'high': 3, 'very_high': 4}
        return scores.get(self.interest, 2)
    
    @property
    def priority_score(self):
        """Calculate priority based on influence and interest"""
        return self.influence_score * self.interest_score


class Engagement(models.Model):
    TYPE_CHOICES = [
        ('meeting', 'Meeting'),
        ('email', 'Email'),
        ('phone', 'Phone Call'),
        ('presentation', 'Presentation'),
        ('workshop', 'Workshop'),
        ('survey', 'Survey'),
        ('interview', 'Interview'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
    ]
    
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]
    
    # Basic Information
    stakeholder = models.ForeignKey(Stakeholder, on_delete=models.CASCADE, related_name='engagements')
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='meeting')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    
    # Timing
    scheduled_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    
    # Content
    description = models.TextField(blank=True)
    objectives = models.TextField(blank=True)
    outcomes = models.TextField(blank=True)
    action_items = models.TextField(blank=True)
    
    # Analysis
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, blank=True)
    effectiveness_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=True,
        null=True,
        help_text="Rate effectiveness from 1-5"
    )
    
    # AI Features
    ai_summary = models.TextField(blank=True, help_text="AI-generated summary of the engagement")
    ai_action_items = models.TextField(blank=True, help_text="AI-extracted action items")
    ai_sentiment_analysis = models.TextField(blank=True, help_text="AI sentiment analysis")
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='engagements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    class Meta:
        ordering = ['scheduled_date']  # Nearest dates first (ascending order)
    
    def __str__(self):
        return f"{self.title} - {self.stakeholder.name} ({self.scheduled_date.strftime('%Y-%m-%d')})"


class StakeholderRelationship(models.Model):
    """Track relationships between stakeholders"""
    RELATIONSHIP_TYPES = [
        ('reports_to', 'Reports To'),
        ('manages', 'Manages'),
        ('collaborates', 'Collaborates With'),
        ('influences', 'Influences'),
        ('depends_on', 'Depends On'),
        ('conflicts', 'Has Conflict With'),
        ('supports', 'Supports'),
    ]
    
    from_stakeholder = models.ForeignKey(
        Stakeholder, 
        on_delete=models.CASCADE, 
        related_name='relationships_from'
    )
    to_stakeholder = models.ForeignKey(
        Stakeholder, 
        on_delete=models.CASCADE, 
        related_name='relationships_to'
    )
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_TYPES)
    description = models.TextField(blank=True)
    strength = models.CharField(
        max_length=20,
        choices=[('weak', 'Weak'), ('moderate', 'Moderate'), ('strong', 'Strong')],
        default='moderate'
    )
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['from_stakeholder', 'to_stakeholder', 'relationship_type']
    
    def __str__(self):
        return f"{self.from_stakeholder.name} {self.get_relationship_type_display()} {self.to_stakeholder.name}"


class DemoSession(models.Model):
    """Track demo mode for users"""
    DEMO_SCENARIOS = [
        ('standard', 'Standard Demo'),
        ('tech_startup', 'Tech Startup'),
        ('enterprise_project', 'Enterprise Project'),
        ('product_launch', 'Product Launch'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='demo_session')
    is_demo_mode = models.BooleanField(default=False)
    demo_started_at = models.DateTimeField(auto_now_add=True)
    demo_scenario = models.CharField(max_length=50, choices=DEMO_SCENARIOS, default='standard')
    
    def __str__(self):
        return f"Demo Session for {self.user.username} - {self.get_demo_scenario_display()}"
