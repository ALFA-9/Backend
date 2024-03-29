# flake8: noqa
import os
from pathlib import Path

from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "SECRET_KEY", "83(vot%*rpken0wm#0lt!defrrf0%%=hl$ey8(b20%l8a07#f^"
)  # default key is just for django test
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost 127.0.0.1").split(" ")

CURRENT_BASE = os.getenv("CURRENT_BASE", "postgre").lower()

HOST_URL = os.getenv("HOST_URL", "http://localhost:8000")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "debug_toolbar",
    "django_filters",
    "drf_spectacular",
    "django_celery_beat",
    "mptt",
    "idps",
    "tasks",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    # Меняется конечная цифра в зависимости от старта контейнеров
    INTERNAL_IPS = [ip[: ip.rfind(".")] + f".{x}" for ip in ips for x in range(1, 5)] + [
        "127.0.0.1",
    ]

    INSTALLED_APPS.insert(6, "corsheaders")
    MIDDLEWARE.insert(2, "corsheaders.middleware.CorsMiddleware")

    CORS_ALLOW_ALL_ORIGINS = True
    CSRF_TRUSTED_ORIGINS = [os.getenv("HOST_URL")] if os.getenv("HOST_URL") else []

SPECTACULAR_SETTINGS = {
    "TITLE": "Alfa People",
    "VERSION": "1.0.5",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVERS": [{"url": HOST_URL}],
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_FAVICON_HREF": (HOST_URL + "/media/logo.svg"),
}

REST_FRAMEWORK = {
    "DATE_INPUT_FORMATS": ["%d.%m.%Y"],
    "DATETIME_FORMAT": "%d.%m.%Y",
    "DATE_FORMAT": "%d.%m.%Y",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

ROOT_URLCONF = "alpha_project.urls"

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

WSGI_APPLICATION = "alpha_project.wsgi.application"

DATABASES = {
    "postgre": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "django_dev"),
        "USER": os.getenv("POSTGRES_USER", "django_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "django_pass"),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": os.getenv("DB_PORT", 5432),
    },
    "lite": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}
DATABASES["default"] = DATABASES[CURRENT_BASE]

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

CELERY_BROKER_URL = os.environ.get("BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("RESULT_BACKEND", "redis://redis:6379/0")
CELERY_BEAT_SCHEDULE = {
    "Status updater for tasks": {
        "task": "tasks.celery_tasks.update_status_for_task",
        "schedule": crontab("0", "0"),
    },
    "Status updater for idps": {
        "task": "idps.celery_tasks.update_status_for_idp",
        "schedule": crontab("0", "1"),
    },
    "Send emails for directors": {
        "task": "users.celery_tasks.send_daily_email",
        "schedule": crontab("0", "15"),
    },
}
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_TIMEZONE = "UTC"

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "collected_static"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.Employee"

EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_HOST_USER", "alpha_idp_service@alpha.ru")
if os.getenv("USE_SMTP", "False").lower() == "true":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL")
