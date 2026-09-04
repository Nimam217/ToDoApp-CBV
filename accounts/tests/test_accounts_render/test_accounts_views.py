'''import pytest
from django.urls import reverse
from django.test import RequestFactory

from accounts.views import (
    RegisterView,
    CustomLoginView,
    LogoutConfirmView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    PasswordChangeView,
    PasswordChangeConfirmView,
    ProfileView,
    ProfileUpdateView,
)


@pytest.mark.django_db
class TestRegisterView:

    def test_get(self, client):
        response = client.get(reverse("accounts:register"))

        assert response.status_code == 200
        assert isinstance(response.context["form"], object)

    def test_view_class(self, client):
        response = client.get(reverse("accounts:register"))

        assert isinstance(response.resolver_match.func.view_class(), RegisterView)


@pytest.mark.django_db
class TestLoginView:

    def test_get(self, client):
        response = client.get(reverse("accounts:login"))

        assert response.status_code == 200

    def test_uses_custom_authentication_form(self):
        assert CustomLoginView.authentication_form.__name__ == "CustomAuthenticationForm"


@pytest.mark.django_db
class TestLogoutConfirmView:

    def test_get(self, client):
        response = client.get(reverse("accounts:logout_confirm"))

        assert response.status_code == 200


@pytest.mark.django_db
class TestPasswordResetView:

    def test_get(self, client):
        response = client.get(reverse("accounts:password_reset"))

        assert response.status_code == 200
        assert "form" in response.context


@pytest.mark.django_db
class TestPasswordResetConfirmView:

    def test_invalid_token(self, client):
        url = reverse(
            "accounts:password_reset_confirm",
            kwargs={
                "uidb64": "invalid",
                "token": "invalid-token",
            },
        )

        response = client.get(url)

        assert response.status_code == 200


@pytest.mark.django_db
class TestPasswordChangeView:

    def test_unauthenticated(self, client):
        response = client.get(reverse("accounts:password_change"))

        assert response.status_code == 302

    def test_authenticated(self, client, verified_user):
        client.force_login(verified_user)

        response = client.get(reverse("accounts:password_change"))

        assert response.status_code == 200


@pytest.mark.django_db
class TestPasswordChangeConfirmView:

    def test_unauthenticated(self, client):
        response = client.get(reverse("accounts:password_change_done"))

        assert response.status_code == 302

    def test_authenticated(self, client, verified_user):
        client.force_login(verified_user)

        response = client.get(reverse("accounts:password_change_done"))

        assert response.status_code == 200


@pytest.mark.django_db
class TestProfileView:

    def test_unauthenticated(self, client, user):
        url = reverse(
            "accounts:profile",
            kwargs={"pk": user.profile.pk},
        )

        response = client.get(url)

        assert response.status_code == 302

    def test_authenticated_owner(self, client, verified_user):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile",
            kwargs={"pk": verified_user.profile.pk},
        )

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["profile"] == verified_user.profile

    def test_other_user_profile(self, client, verified_user, another_user):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile",
            kwargs={"pk": another_user.profile.pk},
        )

        response = client.get(url)

        assert response.status_code == 404


@pytest.mark.django_db
class TestProfileUpdateView:

    def test_unauthenticated(self, client, user):
        url = reverse(
            "accounts:profile_edit",
            kwargs={"pk": user.profile.pk},
        )

        response = client.get(url)

        assert response.status_code == 302

    def test_authenticated_owner(self, client, verified_user):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile_edit",
            kwargs={"pk": verified_user.profile.pk},
        )

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["form"].instance == verified_user.profile

    def test_other_user_profile(self, client, verified_user, another_user):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile_edit",
            kwargs={"pk": another_user.profile.pk},
        )
'''