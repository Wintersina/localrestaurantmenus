"""Production settings for localrestaurantmenus_project."""

from .base import *  # noqa: F401,F403

DEBUG = False

raw_prod_db_url = os.environ.get("DATABASE_URL") or os.environ.get("TEMP_DATABASE_URL")

if raw_prod_db_url:
    DATABASES = {
        "default": dj_database_url.config(default=raw_prod_db_url, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "temp.db",  # type: ignore[name-defined]
        }
    }

# Trust Cloud Run's HTTPS termination
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
