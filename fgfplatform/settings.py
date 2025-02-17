import os
from dotenv import load_dotenv
from datetime import timedelta
from pathlib import Path

from urllib.parse import urlparse


from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

load_dotenv()


# Load environment variables from the .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

#ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
ALLOWED_HOSTS = ['*']
# Application definition
INSTALLED_APPS = [
    # Django built-in apps (should always be at the top)
    'unfold',
    "unfold.contrib.forms",
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',  # Ensure this is only listed once

    # Third-party apps
    'grappelli',
    'colorfield',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_yasg',
    'django_filters',
    'import_export',

    # Custom apps (your own apps)
    'accounts',
    'plants',
    'cultures',
    'animals',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # This line should be included
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'fgfplatform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'fgfplatform.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / os.getenv('DATABASE_NAME', 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Kampala'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'  

# Central directory for static files (for development)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "animals", "static"),  # Animals app static files
    os.path.join(BASE_DIR, "cultures", "static"),  # Cultures app static files
    os.path.join(BASE_DIR, "plants", "static"),  # Plants app static files
]

# Directory where static files are collected (for deployment)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  

# Media files (Uploaded files)
MEDIA_URL = '/media/'  
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.FgfUser'

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Number of records per page
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',  # Add this line
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=72
    ),  # Increased time for access token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Extended refresh token lifetime
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')

SITE_ID = 1

X_FRAME_OPTIONS = 'SAMEORIGIN'  # Add this line
SILENCED_SYSTEM_CHECKS = ['security.W019']  # Add this line

# notes, change access token later

GRAPPELLI_ADMIN_TITLE = "FGF BIODIVERSITY PLATFORM"
GRAPPELLI_SWITCH_USER = True
GRAPPELLI_AUTOCOMPLETE_LIMIT = 10

UNFOLD = {
    "SITE_TITLE": " FGF BIODIVERSITY PLATFORM",
    "SITE_HEADER": "FGF Biodiversity Platform",
    "SITE_SUBHEADER": "ADMIN DASHBOARD ",
    "SITE_DROPDOWN": [],
    "SHOW_HISTORY": True, # show/hide "History" button, default: True
    "SHOW_BACK_BUTTON": False,
    "SHOW_LANGUAGES": True,
}

LANGUAGE_CODE = "en"

USE_I18N = True

LANGUAGES = [
    ('en', _('English')),
    ('sw', _('Swahili')),

]


LANGUAGES = (
    ("de", _("German")),
    ("en", _("English")),

)
