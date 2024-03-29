"""
Django settings for quexl project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/


ALLOWED_HOSTS = [
    "*",
    "http://localhost:4200",
    "https://quexl-api-staging.herokuapp.com",
]  # TODO Add list of allowed hosts
CORS_ORIGIN_ALLOW_ALL = True  # TODO Change to False
# Application definition

# Application definition
CORS_ORIGIN_WHITELIST = [
    "http://localhost:4200",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rolepermissions",
    "corsheaders",
    # local apps
    "quexl.apps.account",
    "quexl.apps.profiles",
    "quexl.apps.messaging",
    "quexl.apps.services",
    "quexl.apps.orders",
    "quexl.apps.contact",
    "quexl.apps.blog",
    # external apps
    "phonenumber_field",
    "social_django",
    "djmoney",
    "channels",
    "languages",
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

ROLEPERMISSIONS_MODULE = "quexl.apps.roles.roles"

ROOT_URLCONF = "quexl.urls"

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
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ]
        },
    }
]

WSGI_APPLICATION = "quexl.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# configure application environments

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = env.bool("DEBUG", default=False)
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = env.str("SECRET_KEY", "#gy%@@^ySGT@^")

DATABASES = {"default": env.db()}

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "github_actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }

# configure Django Channels
REDIS_URL = env.str("REDIS_URL", "redis://localhost:6379")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [REDIS_URL]},
    }
}
ASGI_APPLICATION = "quexl.routing.application"

# configure email

EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST = env.str("EMAIL_HOST", "")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = env.int("EMAIL_PORT", "")

AUTH_USER_MODEL = "account.User"
SOCIAL_AUTH_POSTGRES_JSONFIELD = (
    True  # Use PostgreSQL JSONB to store extra_data  # noqa E501
)
AUTHENTICATION_BACKENDS = (
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env.str("GOOGLE_OAUTH2_KEY", "")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env.str("OAUTH2_SECRET", "")

SOCIAL_AUTH_FACEBOOK_KEY = env.str("FACEBOOK_KEY", "")
SOCIAL_AUTH_FACEBOOK_SECRET = env.str("FACEBOOK_SECRET", "")

SOCIAL_AUTH_FACEBOOK_SCOPE = ["email"]

FACEBOOK_EXTENDED_PERMISSIONS = ["email"]
SOCIAL_AUTH_FACEBOOK_API_VERSION = "3.2"

SOCIAL_AUTH_URL_NAMESPACE = "social-auth"

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/"

REST_FRAMEWORK = {
    "NON_FIELD_ERRORS_KEY": "error",
    # by default every user should be authenticated
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # specifies a local custom authentication class
        "quexl.apps.account.backends.JWTAuthentication",
    ),
    "EXCEPTION_HANDLER": "quexl.utils.exceptions.custom_exception_handler",
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"  # noqa
    },
]

# Test runner
TEST_RUNNER = "quexl.pytest_runner.PytestTestRunner"


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
