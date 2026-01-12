import os
from pathlib import Path

import dj_database_url


def _get_env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_env_list(name, default):
    value = os.getenv(name)
    if value is None:
        value = default
    return [item.strip() for item in value.split(",") if item.strip()]


DEBUG = _get_env_bool("DJANGO_DEBUG", True)

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "dev-insecure-secret"
    else:
        raise RuntimeError("DJANGO_SECRET_KEY is required when DJANGO_DEBUG is false")

ALLOWED_HOSTS = _get_env_list(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,0.0.0.0",
)
CSRF_TRUSTED_ORIGINS = _get_env_list("DJANGO_CSRF_TRUSTED_ORIGINS", "")

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", str(Path.cwd())))
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{PROJECT_ROOT / 'db.sqlite3'}",
        conn_max_age=int(os.getenv("DATABASE_CONN_MAX_AGE", "60")),
    )
}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "{{ cookiecutter.project_slug|replace('-', '_') }}.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "{{ cookiecutter.project_slug|replace('-', '_') }}.server.urls"
WSGI_APPLICATION = "{{ cookiecutter.project_slug|replace('-', '_') }}.server.wsgi.application"
ASGI_APPLICATION = "{{ cookiecutter.project_slug|replace('-', '_') }}.server.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    }
]

LANGUAGE_CODE = os.getenv("DJANGO_LANGUAGE_CODE", "en-us")
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(levelname)s %(name)s %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
    "root": {
        "handlers": ["console"],
        "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
    },
}

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")
CELERY_TASK_ALWAYS_EAGER = _get_env_bool("CELERY_TASK_ALWAYS_EAGER", False)
CELERY_TASK_EAGER_PROPAGATES = _get_env_bool("CELERY_TASK_EAGER_PROPAGATES", True)
CELERY_TASK_DEFAULT_QUEUE = os.getenv("CELERY_TASK_DEFAULT_QUEUE", "default")
CELERY_BEAT_SCHEDULE_FILENAME = os.getenv(
    "CELERY_BEAT_SCHEDULE_FILENAME",
    "/tmp/celerybeat-schedule",
)
CELERY_BEAT_SCHEDULE = {
    "ping-every-60s": {
        "task": "{{ cookiecutter.project_slug|replace('-', '_') }}.core.tasks.ping",
        "schedule": float(os.getenv("CELERY_PING_INTERVAL_SECONDS", "60")),
    },
    "add-every-300s": {
        "task": "{{ cookiecutter.project_slug|replace('-', '_') }}.core.tasks.add",
        "schedule": float(os.getenv("CELERY_ADD_INTERVAL_SECONDS", "300")),
        "args": (2, 3),
    },
}

try:
    from kombu import Exchange, Queue
except Exception:
    Exchange = None
    Queue = None

if Queue is not None:
    CELERY_TASK_QUEUES = (
        Queue(
            CELERY_TASK_DEFAULT_QUEUE,
            Exchange(CELERY_TASK_DEFAULT_QUEUE),
            routing_key=CELERY_TASK_DEFAULT_QUEUE,
        ),
        Queue("high", Exchange("high"), routing_key="high"),
    )

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = _get_env_bool("DJANGO_SECURE_SSL_REDIRECT", True)
    SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_SECURE_HSTS_SECONDS", "60"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_SSL_REDIRECT = _get_env_bool("DJANGO_SECURE_SSL_REDIRECT", False)
