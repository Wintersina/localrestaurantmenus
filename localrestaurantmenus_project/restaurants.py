"""Static config of restaurants served by the site.

Each restaurant has a slug (used in the URL), a display name, the list of
menu page image filenames (rendered inline in order), and the bundled PDF
filename. All asset paths are relative to ``static/menus/<slug>/``.

Add a new restaurant by appending an entry here and dropping its assets into
``static/menus/<slug>/``. No DB, no admin, no migrations.
"""
from collections import OrderedDict


RESTAURANTS = OrderedDict(
    [
        (
            "ehsanis-hot-kabob",
            {
                "name": "Ehsani's Hot Kabob",
                "pages": [
                    "001.webp",
                    "002.webp",
                    "003.webp",
                    "004.webp",
                    "005.webp",
                    "006.webp",
                    "007.webp",
                    "008.webp",
                ],
                "pdf": "ehsanis-hot-kabob.pdf",
            },
        ),
    ]
)


def get_restaurant(slug):
    """Return restaurant config for the given slug, or None."""
    return RESTAURANTS.get(slug)
