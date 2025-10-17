"""
Django settings for Meeting Summarizer project.

This settings file configures the Meeting Summarizer application with:
- Template and static file handling
- Media file uploads (audio files)
- OpenAI API integration
- File upload limits (100MB max)
- Session management for processing status tracking

Generated on: October 13, 2025
"""

# ============================================
# 1. IMPORT NECESSARY MODULES
# ============================================
from pathlib import Path
import os
import sys

# Environment variable management (install: pip install python-decouple)
try:
    from decouple import config
except ImportError:
    # Fallback if python-decouple is not installed
    def config(key, default='', cast=str):
        return os.environ.get(key, default)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================
# SECURITY SETTINGS
# ============================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-meeting-summarizer-dev-key-change-in-production-2025')

# ============================================
# 10. DEBUG SETTINGS
# ============================================

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# ============================================
# 7. ALLOWED HOSTS FOR DEVELOPMENT
# ============================================

# Get allowed hosts from environment variable or use defaults
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,unthinkable-meeting-summarizer-production.up.railway.app,*.up.railway.app').split(',')


# ============================================
# 2. APPLICATION DEFINITION - INSTALLED APPS
# ============================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # For humanize template filters like intcomma
    
    # Third-party apps (optional, add if needed)
    # 'rest_framework',  # For API development
    # 'corsheaders',     # For CORS handling
    
    # Local apps
    'meetings',  # Meeting Summarizer app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files efficiently
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ============================================
# 3. TEMPLATES CONFIGURATION
# ============================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Project-level templates directory
        ],
        'APP_DIRS': True,  # Look for templates in app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # For media files
                'django.template.context_processors.static',  # For static files
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ============================================
# DATABASE CONFIGURATION
# ============================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Alternative: PostgreSQL configuration (uncomment if needed)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME', default='meeting_summarizer'),
#         'USER': config('DB_USER', default='postgres'),
#         'PASSWORD': config('DB_PASSWORD', default=''),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='5432'),
#     }
# }


# ============================================
# PASSWORD VALIDATION
# ============================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ============================================
# INTERNATIONALIZATION
# ============================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = config('TIME_ZONE', default='UTC')

USE_I18N = True

USE_TZ = True


# ============================================
# 4. STATIC FILES CONFIGURATION
# ============================================

# URL to access static files in browser
STATIC_URL = '/static/'

# Directories where Django looks for static files
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Directory where collectstatic gathers all static files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Static file finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# WhiteNoise configuration for efficient static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ============================================
# 5. MEDIA FILES CONFIGURATION
# ============================================

# URL to access media files (uploaded files) in browser
MEDIA_URL = '/media/'

# Directory where uploaded files are stored
MEDIA_ROOT = BASE_DIR / 'media'

# Create media directory if it doesn't exist
os.makedirs(MEDIA_ROOT, exist_ok=True)


# ============================================
# 8. FILE UPLOAD SETTINGS
# ============================================

# Maximum size for files uploaded via forms (100MB in bytes)
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB

# Maximum size for request body (100MB in bytes)
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB

# Directory for temporary file uploads
FILE_UPLOAD_TEMP_DIR = BASE_DIR / 'media' / 'temp'
os.makedirs(FILE_UPLOAD_TEMP_DIR, exist_ok=True)

# File upload handlers
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# Allowed audio file extensions
ALLOWED_AUDIO_EXTENSIONS = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']

# Maximum audio duration in seconds (optional validation)
MAX_AUDIO_DURATION = 7200  # 2 hours


# ============================================
# 6. OPENAI-COMPATIBLE API CONFIGURATION (LLAMA MAVERICK)
# ============================================

# Llama Maverick API key (OpenAI-compatible)
OPENAI_API_KEY = config('OPENAI_API_KEY')

# Llama Maverick base URL (OpenAI-compatible endpoint)
OPENAI_BASE_URL = config('OPENAI_BASE_URL', default='https://openrouter.ai/api/v1')

# Model configurations (use Llama models or OpenAI-compatible models)
OPENAI_WHISPER_MODEL = config('OPENAI_WHISPER_MODEL', default='whisper-1')
OPENAI_GPT_MODEL = config('OPENAI_GPT_MODEL', default='meta-llama/llama-3.1-8b-instruct')

# API settings
OPENAI_TIMEOUT = config('OPENAI_TIMEOUT', default=300, cast=int)  # 5 minutes
OPENAI_MAX_RETRIES = config('OPENAI_MAX_RETRIES', default=3, cast=int)

# ============================================
# GROQ API CONFIGURATION (FREE WHISPER TRANSCRIPTION)
# ============================================

# Groq API key for FREE Whisper transcription
# IMPORTANT: Set this in your .env file, never commit API keys to version control!
# Get your free API key from: https://console.groq.com/keys
GROQ_API_KEY = config('GROQ_API_KEY')

# Groq settings
GROQ_WHISPER_MODEL = config('GROQ_WHISPER_MODEL', default='whisper-large-v3')
GROQ_BASE_URL = 'https://api.groq.com/openai/v1'  # Groq's OpenAI-compatible endpoint


# ============================================
# 9. SESSION CONFIGURATION FOR STATUS TRACKING
# ============================================

# Session engine (default is database-backed sessions)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Alternative: Cache-backed sessions (faster for status polling)
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Session cookie settings
SESSION_COOKIE_NAME = 'meeting_summarizer_sessionid'
SESSION_COOKIE_AGE = 86400  # 24 hours (in seconds)
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)  # Set True in production with HTTPS

# Session for anonymous users (for tracking upload/processing status)
SESSION_COOKIE_SAMESITE = 'Lax'


# ============================================
# CACHE CONFIGURATION (for status tracking)
# ============================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'meeting-summarizer-cache',
        'TIMEOUT': 3600,  # 1 hour default timeout
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# Alternative: Redis cache (recommended for production)
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         },
#         'KEY_PREFIX': 'meeting_summarizer',
#         'TIMEOUT': 3600,
#     }
# }


# ============================================
# LOGGING CONFIGURATION
# ============================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'debug.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': config('LOG_LEVEL', default='INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'meetings': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Create logs directory
os.makedirs(BASE_DIR / 'logs', exist_ok=True)


# ============================================
# CELERY CONFIGURATION (Optional - for async tasks)
# ============================================

# Uncomment if using Celery for background processing
# CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
# CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = TIME_ZONE
# CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes


# ============================================
# REST FRAMEWORK CONFIGURATION (Optional)
# ============================================

# Uncomment if using Django REST Framework for API
# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.AllowAny',
#     ],
#     'DEFAULT_RENDERER_CLASSES': [
#         'rest_framework.renderers.JSONRenderer',
#         'rest_framework.renderers.BrowsableAPIRenderer',
#     ],
#     'DEFAULT_PARSER_CLASSES': [
#         'rest_framework.parsers.JSONParser',
#         'rest_framework.parsers.MultiPartParser',
#         'rest_framework.parsers.FormParser',
#     ],
# }


# ============================================
# CORS CONFIGURATION (Optional)
# ============================================

# Uncomment if allowing cross-origin requests
# CORS_ALLOWED_ORIGINS = config(
#     'CORS_ALLOWED_ORIGINS',
#     default='http://localhost:3000,http://127.0.0.1:3000',
#     cast=lambda v: [s.strip() for s in v.split(',')]
# )
# CORS_ALLOW_CREDENTIALS = True


# ============================================
# SECURITY SETTINGS FOR PRODUCTION
# ============================================

# CSRF trusted origins for Railway deployment
CSRF_TRUSTED_ORIGINS = [
    'https://unthinkable-meeting-summarizer-production.up.railway.app',
    'https://*.up.railway.app',
]

# Uncomment these in production
if not DEBUG:
    # HTTPS/SSL
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Other security headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'


# ============================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ============================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================
# CUSTOM APPLICATION SETTINGS
# ============================================

# Meeting Summarizer specific settings
MEETING_SUMMARIZER = {
    'MAX_FILE_SIZE_MB': 100,
    'SUPPORTED_FORMATS': ['mp3', 'wav', 'm4a', 'ogg', 'flac'],
    'PROCESSING_TIMEOUT': 600,  # 10 minutes
    'ENABLE_AUTO_DELETE': config('ENABLE_AUTO_DELETE', default=False, cast=bool),
    'AUTO_DELETE_DAYS': config('AUTO_DELETE_DAYS', default=30, cast=int),
    'RESULTS_PER_PAGE': 12,  # Pagination for meetings list
}


# ============================================
# DEVELOPMENT HELPERS
# ============================================

# Show detailed error pages in development
if DEBUG:
    INTERNAL_IPS = [
        '127.0.0.1',
        'localhost',
    ]
    
    # Django Debug Toolbar (optional - install: pip install django-debug-toolbar)
    # INSTALLED_APPS += ['debug_toolbar']
    # MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']


# ============================================
# PRODUCTION SECURITY SETTINGS
# ============================================

# Security settings for production
if not DEBUG:
    # HTTPS settings
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Other security settings
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'


# ============================================
# ENVIRONMENT CONFIGURATION SUMMARY
# ============================================
# Configuration summary available in Django startup
# Run with --verbosity 2 to see detailed settings