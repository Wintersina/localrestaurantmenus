import html

from django.urls import reverse


def _body(response):
    return html.unescape(response.content.decode())


def test_home_lists_known_restaurants(client):
    response = client.get(reverse("home"))
    assert response.status_code == 200
    body = _body(response)
    assert "Ehsani's Hot Kabob" in body
    assert 'href="/ehsanis-hot-kabob/"' in body


def test_home_has_noindex(client):
    response = client.get(reverse("home"))
    assert 'name="robots"' in response.content.decode()


def test_restaurant_page_renders_all_menu_pages(client):
    response = client.get(reverse("restaurant", args=["ehsanis-hot-kabob"]))
    assert response.status_code == 200
    body = _body(response)
    assert "Ehsani's Hot Kabob" in body
    for n in range(1, 9):
        assert f"00{n}.webp" in body
    assert "ehsanis-hot-kabob.pdf" in body
    assert 'loading="lazy"' in body
    assert 'loading="eager"' in body


def test_restaurant_page_uses_per_restaurant_favicon(client):
    response = client.get(reverse("restaurant", args=["ehsanis-hot-kabob"]))
    body = _body(response)
    assert 'rel="icon"' in body
    assert "menus/ehsanis-hot-kabob/favicon.ico" in body
    assert "menus/ehsanis-hot-kabob/apple-touch-icon.png" in body
    assert "data:image/svg+xml" not in body  # emoji fallback should be replaced


def test_unknown_restaurant_returns_404(client):
    response = client.get("/no-such-place/")
    assert response.status_code == 404


def test_favicon_served_inline(client):
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    assert response["Content-Type"] == "image/svg+xml"
    assert b"<svg" in response.content
    assert "max-age=" in response["Cache-Control"]
