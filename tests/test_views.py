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


def test_unknown_restaurant_returns_404(client):
    response = client.get("/no-such-place/")
    assert response.status_code == 404
