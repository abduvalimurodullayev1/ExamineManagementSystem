import os
from pathlib import Path

import environ
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))
FCM_API_KEY = env.str("FCM_API_KEY")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = ["*"]
import os

# settings.py
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, "firebase_admin.json")

# Application definition
DJANGO_APPS = [
    "jazzmin",
    "django.contrib.admin",
    'debug_toolbar',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

]

CUSTOM_APPS = [
    # "common",
    # 'common.apps.CommonConfig',
    "apps.users",
    "apps.exam",
    "apps.notification",
    "apps.common",


]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_yasg",
    "corsheaders",
    "modeltranslation",
    'rosetta'
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",
                                 'rest_framework.renderers.BrowsableAPIRenderer',),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS + THIRD_PARTY_APPS
USER_MODEL = 'users.User'
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]
INTERNAL_IPS = [
    '127.0.0.1',
]
ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'django.template.context_processors.i18n'
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
AUTH_USER_MODEL = 'users.User'
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE"),
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.get_value("DB_PASSWORD"),
        "HOST": env.str("DB_HOST"),
        "PORT": env.str("DB_PORT"),
        "ATOMIC_REQUESTS": True,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = (BASE_DIR / "staticfiles",)

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CACHES
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

REDIS_HOST = env.str("REDIS_HOST", "localhost")
REDIS_PORT = env.int("REDIS_PORT", 6379)
REDIS_DB = env.int("REDIS_DB", 0)

# CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", "redis://localhost:6379")
# CELERY_RESULT_BACKEND = env.str("CELERY_BROKER_URL", "redis://localhost:6379")

CELERY_TIMEZONE = "Asia/Tashkent"

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

AES_KEY = env.str("AES_KEY", "")
from django.utils.translation import gettext_lazy as _

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('uz', _('Uzbek')),
    ('ru', _('Russian')),
    ('en', _('English')),
    ('de', _('German')),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'
MODELTRANSLATION_LANGUAGES = ('uz', 'ru', 'en', 'de')
MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': ('en', 'uz'),
    'uz': ('ru', 'en'),
    'de': ('en',),
}

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

from datetime import timedelta

...

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=56),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

LOGIN_URL = '/admin'

LOGOUT_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    # 'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
EMAIL_HOST = env.str("EMAIL_HOST", "localhost")
EMAIL_PORT = env.int("EMAIL_PORT", 25)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", False)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", False)
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

from datetime import timedelta

ONESIGNAL_AUTH_KEY = env.str("ONESIGNAL_AUTH_KEY")
ONESIGNAL_APP_ID = env.str("ONESIGNAL_APP_ID")
ONESIGNAL_REST_KEY = env.str("ONESIGNAL_REST_KEY")


