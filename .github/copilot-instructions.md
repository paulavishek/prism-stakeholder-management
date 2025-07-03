<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Stakeholder Management System - Copilot Instructions

## Project Overview
This is a Django-based stakeholder management web application with AI integration using Google's Gemini API. The system helps users manage stakeholder relationships, track engagements, and provides AI-powered insights.

## Key Technologies
- **Backend**: Django 5.2.3, Python 3.12+
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: Django ORM with SQLite (dev) / PostgreSQL (prod)
- **AI Integration**: Google Gemini API (gemini-1.5-flash)
- **Visualization**: Chart.js

## Project Structure
```
stakeholder_management/        # Main Django project
├── stakeholders/             # Core stakeholder management app
├── ai_assistant/            # AI service integration
├── templates/               # HTML templates
│   ├── base.html           # Base template with Bootstrap
│   ├── auth/               # Authentication templates
│   └── stakeholders/       # Stakeholder-specific templates
├── static/                 # Static files (CSS, JS, images)
└── media/                  # User uploads
```

## Code Style Guidelines

### Python/Django
- Follow PEP 8 style guidelines
- Use Django best practices for models, views, and templates
- Implement proper error handling and validation
- Use Django's built-in authentication and security features
- Keep business logic in models and services, not views

### Models
- Use descriptive field names and help_text
- Implement proper relationships with appropriate on_delete behaviors
- Add validation methods when needed
- Include __str__ methods for better admin interface

### Views
- Use function-based views with decorators for simplicity
- Always require login with @login_required for protected views
- Filter querysets by user to ensure data isolation
- Handle both GET and POST requests appropriately

### Templates
- Extend from base.html for consistency
- Use Bootstrap 5 classes for styling
- Implement responsive design patterns
- Include proper CSRF tokens in forms
- Use template filters for data formatting

### JavaScript
- Use vanilla JavaScript or minimal jQuery
- Implement proper error handling for AJAX calls
- Provide visual feedback for user actions
- Use modern ES6+ features when appropriate

## AI Integration Guidelines

### Gemini Service
- Always check if AI service is available before making calls
- Implement proper error handling and fallbacks
- Use structured prompts for consistent results
- Store AI-generated content in appropriate model fields

### AI Features Implementation
- Provide user control over AI feature usage
- Show loading states during AI processing
- Allow manual editing of AI-generated content
- Implement rate limiting for API calls

## UI/UX Guidelines

### Interactive Elements
- Use hover effects for better user feedback
- Implement tooltips for complex UI elements
- Provide keyboard navigation support
- Use consistent color schemes and spacing

### Data Visualization
- Use Chart.js for consistent chart styling
- Implement interactive elements (hover, click)
- Provide mobile-friendly chart experiences
- Use appropriate chart types for data representation

### Forms
- Use Bootstrap form classes for consistency
- Provide clear validation messages
- Implement progressive enhancement
- Include helpful placeholder text and labels

## Security Considerations
- Always validate user input
- Use Django's CSRF protection
- Implement proper authentication checks
- Sanitize AI-generated content before display
- Use environment variables for sensitive configuration

## Performance Guidelines
- Use Django's pagination for large datasets
- Implement database query optimization
- Use caching where appropriate
- Minimize API calls to external services
- Optimize static file delivery

## Testing Approach
- Write unit tests for models and services
- Test AI integration with mock responses
- Implement integration tests for critical workflows
- Test responsive design across devices

## Common Patterns

### Model Creation
```python
class ModelName(models.Model):
    # Fields with descriptive names
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
```

### View Pattern
```python
@login_required
def view_name(request):
    objects = Model.objects.filter(created_by=request.user)
    # Process logic
    return render(request, 'template.html', context)
```

### AI Service Integration
```python
def ai_enhanced_feature(data):
    gemini_service = GeminiService()
    if gemini_service.is_available():
        return gemini_service.method(data)
    return fallback_response
```

## When Contributing
- Maintain the existing code style and patterns
- Add appropriate error handling
- Update documentation for new features
- Test AI features with and without API access
- Ensure mobile responsiveness
- Follow the established project structure
