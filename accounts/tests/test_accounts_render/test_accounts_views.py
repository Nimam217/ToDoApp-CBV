import pytest
from django.urls import reverse

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

# ============================================================
# Register
# ============================================================


@pytest.mark.django_db
class TestRegisterView:

    def test_get(self, client):
        response = client.get(reverse("accounts:register"))

        assert response.status_code == 200
        assert "form" in response.context

    def test_view_class(self, client):
        response = client.get(reverse("accounts:register"))

        assert response.resolver_match.func.view_class is RegisterView


# ============================================================
# Login
# ============================================================


@pytest.mark.django_db
class TestLoginView:

    def test_get(self, client):
        response = client.get(reverse("accounts:login"))

        assert response.status_code == 200
        assert "form" in response.context

    def test_view_class(self, client):
        response = client.get(reverse("accounts:login"))

        assert response.resolver_match.func.view_class is CustomLoginView

    def test_uses_custom_authentication_form(self):
        assert (
            CustomLoginView.authentication_form.__name__
            == "CustomAuthenticationForm"
        )


# ============================================================
# Logout
# ============================================================


@pytest.mark.django_db
class TestLogoutConfirmView:

    def test_get(self, client):
        response = client.get(reverse("accounts:logout_confirm"))

        assert response.status_code == 200

    def test_view_class(self, client):
        response = client.get(reverse("accounts:logout_confirm"))

        assert response.resolver_match.func.view_class is LogoutConfirmView


# ============================================================
# Password Reset
# ============================================================


@pytest.mark.django_db
class TestPasswordResetView:

    def test_get(self, client):
        response = client.get(reverse("accounts:password_reset"))

        assert response.status_code == 200
        assert "form" in response.context

    def test_view_class(self, client):
        response = client.get(reverse("accounts:password_reset"))

        assert (
            response.resolver_match.func.view_class is CustomPasswordResetView
        )


# ============================================================
# Password Reset Confirm
# ============================================================


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

    def test_view_class(self, client):
        url = reverse(
            "accounts:password_reset_confirm",
            kwargs={
                "uidb64": "invalid",
                "token": "invalid-token",
            },
        )

        response = client.get(url)

        assert (
            response.resolver_match.func.view_class
            is CustomPasswordResetConfirmView
        )


# ============================================================
# Password Change
# ============================================================


@pytest.mark.django_db
class TestPasswordChangeView:

    def test_unauthenticated(self, client):
        response = client.get(reverse("accounts:password_change"))

        assert response.status_code == 302
        assert response.url.startswith(reverse("accounts:login"))

    def test_authenticated(self, client, verified_user):
        client.force_login(verified_user)

        response = client.get(reverse("accounts:password_change"))

        assert response.status_code == 200
        assert "form" in response.context

    def test_view_class(self, client):
        response = client.get(reverse("accounts:password_change"))

        assert response.resolver_match.func.view_class is PasswordChangeView


# ============================================================
# Password Change Confirm
# ============================================================


@pytest.mark.django_db
class TestPasswordChangeConfirmView:

    def test_unauthenticated(self, client):
        response = client.get(reverse("accounts:password_change_done"))

        assert response.status_code == 302
        assert response.url.startswith(reverse("accounts:login"))

    def test_authenticated(self, client, verified_user):
        client.force_login(verified_user)

        response = client.get(reverse("accounts:password_change_done"))

        assert response.status_code == 200

    def test_view_class(self, client):
        response = client.get(reverse("accounts:password_change_done"))

        assert (
            response.resolver_match.func.view_class
            is PasswordChangeConfirmView
        )


# ============================================================
# Profile
# ============================================================


@pytest.mark.django_db
class TestProfileView:

    def test_unauthenticated(self, client, user):
        url = reverse(
            "accounts:profile",
            kwargs={"pk": user.profile.pk},
        )

        response = client.get(url)

        assert response.status_code == 302
        assert response.url.startswith(reverse("accounts:login"))

    def test_authenticated_owner(self, client, verified_user):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile",
            kwargs={"pk": verified_user.profile.pk},
        )

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["profile"] == verified_user.profile

    def test_other_user_profile(
        self,
        client,
        verified_user,
        another_user,
    ):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile",
            kwargs={"pk": another_user.profile.pk},
        )

        response = client.get(url)

        assert response.status_code == 404

    def test_view_class(self, client, verified_user):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile",
            kwargs={"pk": verified_user.profile.pk},
        )

        response = client.get(url)

        assert response.resolver_match.func.view_class is ProfileView


# ============================================================
# Profile Update
# ============================================================


@pytest.mark.django_db
class TestProfileUpdateView:

    def test_unauthenticated(self, client, user):
        url = reverse(
            "accounts:profile_edit",
            kwargs={"pk": user.profile.pk},
        )

        response = client.get(url)

        assert response.status_code == 302
        assert response.url.startswith(reverse("accounts:login"))

    def test_authenticated_owner(self, client, verified_user):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile_edit",
            kwargs={"pk": verified_user.profile.pk},
        )

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["form"].instance == verified_user.profile

    def test_other_user_profile(
        self,
        client,
        verified_user,
        another_user,
    ):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile_edit",
            kwargs={"pk": another_user.profile.pk},
        )

        response = client.get(url)

        assert response.status_code == 404

    def test_view_class(self, client, verified_user):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile_edit",
            kwargs={"pk": verified_user.profile.pk},
        )

        response = client.get(url)

        assert response.resolver_match.func.view_class is ProfileUpdateView
