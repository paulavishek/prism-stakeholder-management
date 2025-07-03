from django import template

register = template.Library()

@register.filter
def status_badge_class(status):
    """Convert engagement status to appropriate Bootstrap badge class"""
    status_map = {
        'planned': 'bg-primary',
        'completed': 'bg-success',
        'cancelled': 'bg-danger',
        'postponed': 'bg-warning',
    }
    return status_map.get(status, 'bg-secondary')

@register.filter
def influence_badge_class(influence):
    """Convert stakeholder influence to appropriate Bootstrap badge class"""
    influence_map = {
        'low': 'bg-secondary',
        'medium': 'bg-info',
        'high': 'bg-warning',
        'very_high': 'bg-danger',
    }
    return influence_map.get(influence, 'bg-secondary')

@register.filter
def interest_badge_class(interest):
    """Convert stakeholder interest to appropriate Bootstrap badge class"""
    interest_map = {
        'low': 'bg-secondary',
        'medium': 'bg-info',
        'high': 'bg-warning',
        'very_high': 'bg-danger',
    }
    return interest_map.get(interest, 'bg-secondary')
