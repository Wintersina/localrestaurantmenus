"""Minimal subset of dj-database-url for offline environments."""

import os
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured


ENGINE_ALIASES = {
    "postgres": "django.db.backends.postgresql",
    "postgresql": "django.db.backends.postgresql",
    "postgresql_psycopg2": "django.db.backends.postgresql",
    "psql": "django.db.backends.postgresql",
    "mysql": "django.db.backends.mysql",
    "sqlite": "django.db.backends.sqlite3",
    "sqlite3": "django.db.backends.sqlite3",
}


def config(env="DATABASE_URL", default=None, conn_max_age=0):
    """Return a Django database settings dictionary parsed from a URL."""

    database_url = os.environ.get(env, default)
    if not database_url:
        raise ImproperlyConfigured("A database URL is required for configuration")

    parsed = urlparse(database_url)
    engine = ENGINE_ALIASES.get(parsed.scheme)
    if not engine:
        raise ImproperlyConfigured(f"Unsupported database schema: {parsed.scheme}")

    name = parsed.path[1:] if parsed.path else ""
    if engine == "django.db.backends.sqlite3":
        name = parsed.path if parsed.path else database_url.replace("sqlite://", "", 1) or ":memory:"

    return {
        "ENGINE": engine,
        "NAME": name,
        "USER": parsed.username or "",
        "PASSWORD": parsed.password or "",
        "HOST": parsed.hostname or "",
        "PORT": str(parsed.port) if parsed.port else "",
        "CONN_MAX_AGE": conn_max_age,
    }
