"""Development settings for localrestaurantmenus_project."""

import copy

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

# Deep-copy before mutating: settings/__init__.py auto-imports this module,
# so a direct mutation would leak the verbose formatter into the production
# settings (they share the same dict object via `from .base import *`).
LOGGING = copy.deepcopy(LOGGING)  # type: ignore[name-defined]
LOGGING["handlers"]["stdout"]["formatter"] = "verbose"
