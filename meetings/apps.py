"""
Django app configuration for meetings application.
"""

from django.apps import AppConfig


class MeetingsConfig(AppConfig):
    """
    Configuration for the meetings application.
    
    This app manages meeting recordings, transcripts, summaries,
    and action items for the Meeting Summarizer project.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'meetings'
    verbose_name = 'Meeting Summarizer'
    
    def ready(self):
        """
        Import signal handlers when the app is ready.
        
        This method is called when Django starts up. Use it to
        register signal handlers or perform other initialization.
        """
        # Import signals if you create a signals.py file
        # import meetings.signals
        pass
