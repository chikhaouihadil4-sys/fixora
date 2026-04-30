"""
Django settings for fixora project.
"""

from pathlib import Path
import os
import dj_database_url
BASE_DIR = Path(__file__).resolve().parent.parent


# -----------------------------
# SECURITY
# -----------------------------

SECRET_KEY = 'django-insecure-0rs(+19$t0r%%85rh!&*fu^+^3$+v5lbabvugun$tlz&s%z'

DEBUG = False

ALLOWED_HOSTS = [
    "fixora-8odh.onrender.com",
    ".onrender.com"
]


# -----------------------------
# INSTALLED APPS
# -----------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main',
]


# -----------------------------
# MIDDLEWARE
# -----------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # مهم جدًا للـ static files
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# -----------------------------
# URLS
# -----------------------------

ROOT_URLCONF = 'fixora.urls'


# -----------------------------
# TEMPLATES
# -----------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'main' / 'templates'],
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


# -----------------------------
# WSGI
# -----------------------------

WSGI_APPLICATION = 'fixora.wsgi.application'


# -----------------------------
# DATABASE
# -----------------------------



DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}


# -----------------------------
# PASSWORD VALIDATION
# -----------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# -----------------------------
# INTERNATIONALIZATION
# -----------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# -----------------------------
# STATIC FILES
# -----------------------------

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# مهم جدًا في Render
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# -----------------------------
# MEDIA FILES
# -----------------------------

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# -----------------------------
# LOGIN
# -----------------------------

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


# -----------------------------
# DEFAULT AUTO FIELD
# -----------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'