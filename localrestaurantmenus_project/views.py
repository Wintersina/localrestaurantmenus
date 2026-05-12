from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from localrestaurantmenus_project.restaurants import RESTAURANTS, get_restaurant


_FAVICON_SVG = (
    b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
    b'<text y=".9em" font-size="90">\xf0\x9f\x8d\xbd\xef\xb8\x8f</text></svg>'
)


@cache_control(public=True, max_age=60 * 60 * 24 * 30)
def favicon(request):
    return HttpResponse(_FAVICON_SVG, content_type="image/svg+xml")


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
