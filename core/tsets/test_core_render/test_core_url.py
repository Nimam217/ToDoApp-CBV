'''from django.urls import resolve, reverse

from core.views import HomeView


def test_home_url():
    url = reverse("core:home")

    assert url == "/"
    assert resolve(url).func.view_class == HomeView'''