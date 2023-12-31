"""
Django settings for ClickWork project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from dotenv import load_dotenv
from rest_framework.settings import api_settings

load_dotenv()
log = logging.getLogger(__name__)
logging.getLogger('faker').setLevel(logging.ERROR)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = [
    ".admin.clik-work.ru",
    ".clik-work.ru",
    "localhost",
    "5.159.100.4",
    "127.0.0.1",
]

DEBUG = os.getenv("DEBUG")


INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mptt",
    "rest_framework",
    "knox",
    "drf_spectacular",
    "django_rest_passwordreset",
    "django_filters",
    "django.contrib.postgres",
    "app.main_users.apps.MainUsersConfig",      # пользователи
    "app.user_docs.apps.UserDocsConfig",        # документы пользователей
    "app.orders.apps.OrdersConfig",             # заказы
    "app.categories.apps.CategoriesConfig",     # категории и специализации
    "app.accounts.apps.AccountsConfig",         # счета и фонды
    "app.contests.apps.ContestsConfig",         # конкурсы
    "app.news.apps.NewsConfig",                 # новости
    "app.portfolio",                            # портфолио
    "app.voiting.apps.VoitingConfig",           # голосование
    "app.tickets.apps.TicketsConfig",           # тикеты
    "app.faq.apps.FaqConfig",                   # faq
    "app.company_docs.apps.CompanyDocsConfig",  # доки платформы и получние реф.ссылки
    "app.reviews",                              # отзывы
    "app.raiting.apps.RaitingConfig",           # рейтинг
    "app.mails.apps.MailsConfig",               # расслыки писем
    "app.orders_comment",                       # комментарии к заказам
    "app.chat.apps.ChatConfig",                 # чат
    "app.adv_cash.apps.AdvCashConfig",          # вывод денег adv cash
    "app.referal_link.apps.ReferalLinkConfig"        # вывод ссылки в порядке очереди
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5174",
]

ROOT_URLCONF = "ClickWork.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "app/main_users/templates/main_users")],
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

WSGI_APPLICATION = "ClickWork.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USERNAME"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "PORT": "5432",
        "HOST": os.getenv("DB_HOST"),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
# STATIC_DIR = os.path.join(BASE_DIR, '/static/')
# STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, "static")


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "../static/media")


AUTH_USER_MODEL = "main_users.CustomUser"

DRF_RECAPTCHA_SECRET_KEY = '6LePNqsoAAAAAPTjHRaXvR-9saKXE2VRxhl78KKV'


REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASSES': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"user": "50/minute", "anon": "40/minute"},
    "DEFAULT_AUTHENTICATION_CLASSES": ("knox.auth.TokenAuthentication",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "ClickWork",
    "DESCRIPTION": "...",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "ENUM_NAME_OVERRIDES": {
        'status': 'CustomStatusEnum'
    }
}

REST_KNOX = {
    "SECURE_HASH_ALGORITHM": "cryptography.hazmat.primitives.hashes.SHA512",
    "AUTH_TOKEN_CHARACTER_LENGTH": 64,
    "TOKEN_TTL": timedelta(hours=10),
    "USER_SERIALIZER": "app.main_users.serializers.CustomUserSerializer",
    "TOKEN_LIMIT_PER_USER": None,
    "AUTO_REFRESH": False,
    "EXPIRY_DATETIME_FORMAT": api_settings.DATETIME_FORMAT,
}


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = "tmp/sent_emails/"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = 25
EMAIL_USE_TLS = True
# SERVER_EMAIL = EMAIL_HOST_USER



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "general.log",
            "maxBytes": 1024 * 1024,
            "backupCount": 30,
            "level": "DEBUG",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["file"],
        },
    },
    "formatters": {
        "verbose": {
            "format": "{name} {levelname} {asctime} {module} {lineno} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
}


# CELERY STUFF
CELERY_BROKER_URL = f'redis://{os.getenv("REDIS_HOST")}:6379/0'
CELERY_RESULT_BACKEND = f'redis://{os.getenv("REDIS_HOST")}:6379/0'
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Africa/Nairobi"

FLAGS = {
    "reg_time": 1,
    "orders": 1,
    "peace_orders": -10,
    "arbit": -50,
    "contest": 10,
    "wins": [50, 40, 10],
    "reviews": [1, -5],
    "reply_time": [0.1, 0.05, -1],
    "vote_participation": [5, -10],
}

ACCEPT_BEST_WORKS = int(os.getenv("ACCEPT_BEST_WORKS"))

ADV_API_NAME=os.getenv("ADV_API_NAME")
ADV_PASSWORD=os.getenv("ADV_PASSWORD")
ADV_IP_ADDRESS=os.getenv("ADV_IP_ADDRESS")
ADV_ACCOUNT_EMAIL=os.getenv("ADV_ACCOUNT_EMAIL")