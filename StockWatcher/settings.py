"""
Django settings for StockWatcher project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["STOCK_WATCHER_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ["APP_ENV"] == "production":
    DEBUG = True
else:
    DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "3773-2607-fea8-3f60-6ff0-20bc-ee8-61a9-7165.ngrok.io",
    "localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3000/home",
    "192.168.0.184",
    "192.168.0.91",
    "0.0.0.0:5100",
    "0.0.0.0",
    "stock-watcher-api.herokuapp.com",
    "jaybenaim.github.io",
    "jaybenaim.github.io/StockWatcherClient",
]

# Application definition

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "markdown",
    "mainApp",
    "firebase_auth",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if os.environ["APP_ENV"] == "production":
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")

ROOT_URLCONF = "StockWatcher.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "StockWatcher.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "static/"),
)
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(filename)s.%(funcName)s:%(lineno)s - %(message)s"
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "stockWatcher_handler": {
            "class": "logging.FileHandler",
            "filename": "StockWatcher/Logs/stocks.debug.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "stockWatcher": {
            "handlers": ["console", "stockWatcher_handler"],
            "level": "DEBUG",
        },
    },
}


if os.environ["APP_ENV"] == "production":
    CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]
else:
    CELERY_BROKER_URL = os.environ["LOCAL_CELERY_BROKER_URL"]


# CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://jaybenaim.github.io",
    "http://192.168.0.184:3000",
    "http://192.168.0.91:3000",
    "https://3773-2607-fea8-3f60-6ff0-20bc-ee8-61a9-7165.ngrok.io",
]
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000.com",
    "http://127.0.0.1:3000.com",
    "http://192.168.0.91:3000/",
]

# CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    "xsrfheadername",
    "xsrfcookiename",
    "content-type",
    "XSRF-TOKEN",
    "X-CSRFTOKEN",
    "http_authorization",
    "authorization",
)

# CSRF_COOKIE_NAME = "X-CSRFTOKEN"
CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_HTTPONLY = False

CORS_EXPOSE_HEADERS = [
    "Content-Type",
    "X-CSRFToken",
    "HTTP_AUTHORIZATION",
    "Authorization",
]
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_NAME = "csrftoken"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "firebase_auth.authentication.FirebaseAuthentication",
        # 'rest_framework.authentication.BasicAuthentication'
        #  'rest_framework.authentication.TokenAuthentication',
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
