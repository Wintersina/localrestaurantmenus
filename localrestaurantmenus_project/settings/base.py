"""Base Django settings for localrestaurantmenus_project."""

import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-change-me")

DEBUG = os.environ.get("DEBUG", "False").lower() in {"1", "true", "yes", "on"}

DEFAULT_ALLOWED_HOSTS = [
    "localrestaurantmenus.xyz",
    "www.localrestaurantmenus.xyz",
    "127.0.0.1",
    "localhost",
]

raw_allowed_hosts = os.environ.get("ALLOWED_HOSTS", "")
env_allowed_hosts = [host.strip() for host in raw_allowed_hosts.split(",") if host.strip()]
ALLOWED_HOSTS = DEFAULT_ALLOWED_HOSTS + [
    host for host in env_allowed_hosts if host not in DEFAULT_ALLOWED_HOSTS
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "localrestaurantmenus_project.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "localrestaurantmenus_project.wsgi.application"


default_db_path = os.environ.get("DJANGO_SQLITE_PATH", BASE_DIR / "db.sqlite3")

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{default_db_path}", conn_max_age=600
    )
}


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise: hashed filenames + far-future Cache-Control on static assets
# (menu PNGs and PDFs) so browsers and CDNs cache aggressively. Falls back to
# uncompressed manifest in production.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
