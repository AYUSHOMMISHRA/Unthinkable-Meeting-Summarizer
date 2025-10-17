"""
Django URL configuration for Meeting Summarizer application.

This module defines URL patterns for the meetings app with RESTful naming
conventions and proper namespacing for reverse URL lookups.

Created on: October 13, 2025
"""

from django.urls import path
from . import views
from .debug_views import debug_meeting

# App namespace for URL reversing
app_name = 'meetings'

# URL patterns
urlpatterns = [
    # Home page - displays upload form
    path('', views.index, name='index'),
    
    # Upload meeting audio file
    path('upload/', views.upload_meeting, name='upload'),
    
    # Processing status page
    path('processing/<int:meeting_id>/', views.processing, name='processing'),
    
    # Meeting detail page - displays transcript, summary, action items
    path('meeting/<int:meeting_id>/', views.meeting_detail, name='detail'),
    
    # List all meetings with pagination
    path('meetings/', views.meetings_list, name='list'),
    
    # Delete a meeting
    path('delete/<int:meeting_id>/', views.delete_meeting, name='delete'),
    
    # Toggle star/favorite status
    path('toggle-star/<int:meeting_id>/', views.toggle_star, name='toggle_star'),
    
    # About page
    path('about/', views.about, name='about'),
    
    # API endpoint - get meeting status (AJAX)
    path('api/status/<int:meeting_id>/', views.get_meeting_status, name='status'),
    
    # Debug endpoint - check meeting data
    path('debug/meeting/<int:meeting_id>/', debug_meeting, name='debug_meeting'),
]
