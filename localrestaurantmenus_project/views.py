from django.http import Http404
from django.shortcuts import render

from localrestaurantmenus_project.restaurants import RESTAURANTS, get_restaurant


def home(request):
    """Plain-text index of restaurant slugs. Intentionally minimal — the
    canonical entry points are QR-code deep links to each restaurant page."""
    return render(
        request,
        "home.html",
        {"restaurants": [(slug, cfg["name"]) for slug, cfg in RESTAURANTS.items()]},
    )


def restaurant(request, slug):
    cfg = get_restaurant(slug)
    if cfg is None:
        raise Http404("Restaurant not found")

    asset_base = f"menus/{slug}/"
    return render(
        request,
        "restaurant.html",
        {
            "slug": slug,
            "name": cfg["name"],
            "page_images": [asset_base + page for page in cfg["pages"]],
            "pdf_path": asset_base + cfg["pdf"],
        },
    )
