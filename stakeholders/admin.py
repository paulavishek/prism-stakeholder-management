from django.contrib import admin
from .models import Stakeholder, Engagement, StakeholderRelationship

@admin.register(Stakeholder)
class StakeholderAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'title', 'influence', 'interest', 'category', 'created_at']
    list_filter = ['influence', 'interest', 'category', 'created_at']
    search_fields = ['name', 'organization', 'title', 'email']
    readonly_fields = ['created_at', 'updated_at', 'ai_generated_insights']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'organization', 'department')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Stakeholder Analysis', {
            'fields': ('influence', 'interest', 'category')
        }),
        ('Additional Details', {
            'fields': ('description', 'notes')
        }),
        ('AI Insights', {
            'fields': ('ai_generated_insights',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    list_display = ['title', 'stakeholder', 'type', 'status', 'scheduled_date', 'created_by']
    list_filter = ['type', 'status', 'sentiment', 'scheduled_date']
    search_fields = ['title', 'stakeholder__name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'ai_summary', 'ai_action_items', 'ai_sentiment_analysis']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('stakeholder', 'title', 'type', 'status')
        }),
        ('Timing', {
            'fields': ('scheduled_date', 'duration_minutes')
        }),
        ('Content', {
            'fields': ('description', 'objectives', 'outcomes', 'action_items')
        }),
        ('Analysis', {
            'fields': ('sentiment', 'effectiveness_rating')
        }),
        ('AI Analysis', {
            'fields': ('ai_summary', 'ai_action_items', 'ai_sentiment_analysis'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(StakeholderRelationship)
class StakeholderRelationshipAdmin(admin.ModelAdmin):
    list_display = ['from_stakeholder', 'relationship_type', 'to_stakeholder', 'strength']
    list_filter = ['relationship_type', 'strength']
    search_fields = ['from_stakeholder__name', 'to_stakeholder__name']
