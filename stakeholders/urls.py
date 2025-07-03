from django.urls import path
from . import views

urlpatterns = [
    # Welcome page (root)
    path('', views.welcome, name='welcome'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Stakeholder URLs
    path('stakeholders/', views.stakeholder_list, name='stakeholder_list'),
    path('stakeholders/create/', views.stakeholder_create, name='stakeholder_create'),
    path('stakeholders/<int:pk>/', views.stakeholder_detail, name='stakeholder_detail'),
    path('stakeholders/<int:pk>/edit/', views.stakeholder_edit, name='stakeholder_edit'),
    path('stakeholders/<int:pk>/delete/', views.stakeholder_delete, name='stakeholder_delete'),
      # Engagement URLs
    path('engagements/', views.engagement_list, name='engagement_list'),
    path('engagements/create/', views.engagement_create, name='engagement_create'),
    path('engagements/<int:pk>/', views.engagement_detail, name='engagement_detail'),
    path('engagements/<int:pk>/edit/', views.engagement_edit, name='engagement_edit'),
    
    # AI Assistant URLs
    path('ai/generate-summary/<int:engagement_pk>/', views.generate_ai_summary, name='generate_ai_summary'),
    path('ai/draft-communication/', views.draft_communication, name='draft_communication'),
    path('ai/meeting-summary/', views.meeting_summary, name='meeting_summary'),
    
    # API endpoints
    path('api/stakeholders/', views.api_stakeholders, name='api_stakeholders'),
    
    # Demo data management
    path('demo/load/', views.load_demo_data, name='load_demo_data'),
    path('demo/clear/', views.clear_demo_data, name='clear_demo_data'),
    path('demo/status/', views.get_demo_status, name='demo_status'),
]
