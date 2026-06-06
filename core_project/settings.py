import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-sambilila-core-vibrant-production-key-2026'

# CRITICAL: Turn off DEBUG in production, let Vercel populate it safely via environment variables
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Explicitly whitelist Vercel and local configurations
ALLOWED_HOSTS = ['.vercel.app', 'localhost', '127.0.0.1', '*']

# --- TENANT CONFIGURATION ---
SHARED_APPS = [
    'django_tenants',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'school', 
    'accounts',
]

TENANT_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'accounts',
    'portals',
    'assessments',
    'attendance',
    'school',
]

# Ensure django_tenants is the very first entry
INSTALLED_APPS = ['django_tenants'] + [
    app for app in dict.fromkeys(SHARED_APPS + TENANT_APPS) 
    if app != 'django_tenants'
]

TENANT_MODEL = "school.Client"
TENANT_DOMAIN_MODEL = "school.Domain"

# --- MIDDLEWARE & TEMPLATES ---
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware', # MUST be first
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Added here to intercept and compress static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --- DATABASE CONFIGURATION ---
# NOTE: Your local localhost credentials won't connect from Vercel's servers.
# Use an external production PostgreSQL instance (like Supabase or Neon) and supply its URI string inside Vercel's Environment Variables.
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:1402@127.0.0.1:5432/sambilila_db',
        engine='django_tenants.postgresql_backend'
    )
}

# Where to send users after a successful login if no '?next=' parameter is present
LOGIN_REDIRECT_URL = '/admin/'  

# Where to send users if they try to access a protected page while logged out
LOGIN_URL = '/'

DATABASE_ROUTERS = ('django_tenants.routers.TenantSyncRouter',)

# --- CORE CONFIGURATION ---
ROOT_URLCONF = 'core_project.urls'
PUBLIC_SCHEMA_URLCONF = 'core_project.public_urls'
AUTH_USER_MODEL = 'accounts.CustomUser'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# --- MISC ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lusaka'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- STATIC FILES CONFIGURATION (WhiteNoise Serverless setup) ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Keep storage simple for development, swap to WhiteNoise storage handling on production/Vercel environments
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
