"""
Health check view for Railway deployment.

This view helps diagnose configuration issues by checking:
- Environment variables
- API key availability
- Service initialization
"""

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
import os


@require_GET
def health_check(request):
    """
    Health check endpoint to verify Railway configuration.
    
    Returns JSON with:
    - Status of required environment variables
    - API service availability
    - Configuration warnings
    """
    
    health_status = {
        'status': 'healthy',
        'checks': {},
        'warnings': [],
        'environment': 'production' if not settings.DEBUG else 'development',
        'deployment_id': 'v1.0.3-redirect-fix',
        'commit': 'f71e160'
    }
    
    # Check GROQ_API_KEY
    groq_key = getattr(settings, 'GROQ_API_KEY', None)
    health_status['checks']['groq_api_key'] = {
        'configured': bool(groq_key),
        'message': 'Groq API key is configured (FREE transcription)' if groq_key else 'Groq API key is missing'
    }
    
    # Check OPENAI_API_KEY
    openai_key = getattr(settings, 'OPENAI_API_KEY', None)
    health_status['checks']['openai_api_key'] = {
        'configured': bool(openai_key),
        'message': 'OpenAI API key is configured' if openai_key else 'OpenAI API key is missing'
    }
    
    # Check if at least one API key is configured
    if not groq_key and not openai_key:
        health_status['status'] = 'unhealthy'
        health_status['warnings'].append(
            'No API keys configured! Set GROQ_API_KEY or OPENAI_API_KEY in Railway Variables.'
        )
    
    # Check SECRET_KEY
    secret_key = settings.SECRET_KEY
    if secret_key and 'django-insecure' in secret_key:
        health_status['warnings'].append(
            'Using default SECRET_KEY! Set a secure SECRET_KEY in Railway Variables.'
        )
    
    # Check DEBUG setting
    if settings.DEBUG and os.environ.get('RAILWAY_ENVIRONMENT'):
        health_status['warnings'].append(
            'DEBUG=True in production! Set DEBUG=False in Railway Variables.'
        )
    
    # Check ALLOWED_HOSTS
    allowed_hosts = settings.ALLOWED_HOSTS
    if not allowed_hosts or allowed_hosts == ['*']:
        health_status['warnings'].append(
            'ALLOWED_HOSTS not properly configured! This may cause security issues.'
        )
    
    # Try to initialize transcription service
    try:
        from meetings.services.transcription_service import TranscriptionService
        transcription_service = TranscriptionService()
        health_status['checks']['transcription_service'] = {
            'status': 'ok',
            'message': f'Transcription service initialized with model: {transcription_service.model}'
        }
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['transcription_service'] = {
            'status': 'error',
            'message': f'Failed to initialize: {str(e)}'
        }
    
    # Try to initialize summarization service
    try:
        from meetings.services.summarization_service import SummarizationService
        summarization_service = SummarizationService()
        health_status['checks']['summarization_service'] = {
            'status': 'ok',
            'message': 'Summarization service initialized successfully'
        }
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['summarization_service'] = {
            'status': 'error',
            'message': f'Failed to initialize: {str(e)}'
        }
    
    # Set HTTP status code
    status_code = 200 if health_status['status'] == 'healthy' else 500
    
    return JsonResponse(health_status, status=status_code, json_dumps_params={'indent': 2})
