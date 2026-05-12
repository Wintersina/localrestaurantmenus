"""Development settings for localrestaurantmenus_project."""

from .base import *  # noqa: F401,F403

DEBUG = True

# In dev, skip the manifest storage so unhashed filenames work without
# running collectstatic on every change.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
