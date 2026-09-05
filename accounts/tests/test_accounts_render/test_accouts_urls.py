"""import pytest
from django.urls import NoReverseMatch, reverse, resolve

from accounts.views import (
    CustomLoginView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
    LogoutConfirmView,
    PasswordChangeConfirmView,
    PasswordChangeView,
    ProfileUpdateView,
    ProfileView,
    RegisterView,
)


@pytest.mark.django_db
class TestAccountsURLs:
    def test_login_url(self):
        url = reverse("accounts:login")

        assert url == "/accounts/login/"
        assert resolve(url).func.view_class == CustomLoginView

    def test_register_url(self):
        url = reverse("accounts:register")

        assert url == "/accounts/register/"
        assert resolve(url).func.view_class == RegisterView

    def test_password_reset_url(self):
        url = reverse("accounts:password_reset")

        assert url == "/accounts/password_reset/"
        assert resolve(url).func.view_class == CustomPasswordResetView

    def test_password_reset_done_url(self):
        url = reverse("accounts:password_reset_done")

        assert url == "/accounts/password_reset/done/"

    def test_password_reset_confirm_url(self):
        url = reverse(
            "accounts:password_reset_confirm",
            kwargs={
                "uidb64": "MQ",
                "token": "test-token",
            },
        )

        assert url == "/accounts/reset/MQ/test-token/"
        assert resolve(url).func.view_class == CustomPasswordResetConfirmView

    def test_password_change_url(self):
        url = reverse("accounts:password_change")

        assert url == "/accounts/password_change/"
        assert resolve(url).func.view_class == PasswordChangeView

    def test_password_change_done_url(self):
        url = reverse("accounts:password_change_done")

        assert url == "/accounts/password_change/done/"
        assert resolve(url).func.view_class == PasswordChangeConfirmView

    def test_logout_confirm_url(self):
        url = reverse("accounts:logout_confirm")

        assert url == "/accounts/logout_confirm/"
        assert resolve(url).func.view_class == LogoutConfirmView

    def test_profile_url(self, user):
        url = reverse(
            "accounts:profile",
            kwargs={"pk": user.profile.pk},
        )

        assert url == f"/accounts/profile/{user.profile.pk}/"
        assert resolve(url).func.view_class == ProfileView

    def test_profile_edit_url(self, user):
        url = reverse(
            "accounts:profile_edit",
            kwargs={"pk": user.profile.pk},
        )

        assert url == f"/accounts/profile/{user.profile.pk}/edit/"
        assert resolve(url).func.view_class == ProfileUpdateView

    def test_accounts_api_namespace(self):
        assert reverse(
            "accounts:accounts-api-v1:registration"
        ) == "/accounts/api/v1/registration/"

        assert reverse(
            "accounts:accounts-api-v1:token_auth"
        ) == "/accounts/api/v1/token-auth/create/"

        assert reverse(
            "accounts:accounts-api-v1:discard_auth_token"
        ) == "/accounts/api/v1/token-auth/discard/"

        assert reverse(
            "accounts:accounts-api-v1:profile"
        ) == "/accounts/api/v1/profile/"

        assert reverse(
            "accounts:accounts-api-v1:token_obtain_pair"
        ) == "/accounts/api/v1/jwt/create/"

        assert reverse(
            "accounts:accounts-api-v1:token_refresh"
        ) == "/accounts/api/v1/jwt/refresh/"

        assert reverse(
            "accounts:accounts-api-v1:token_verify"
        ) == "/accounts/api/v1/jwt/verify/"

        assert reverse(
            "accounts:accounts-api-v1:change_password"
        ) == "/accounts/api/v1/change_password/"

        assert reverse(
            "accounts:accounts-api-v1:reset_password"
        ) == "/accounts/api/v1/reset_password/"

        assert reverse(
            "accounts:accounts-api-v1:reset_password_confirm",
            kwargs={"token": "test-token"},
        ) == "/accounts/api/v1/reset_password/confirm/test-token/"

        assert reverse(
            "accounts:accounts-api-v1:activation_resend"
        ) == "/accounts/api/v1/activation/resend/"

        assert reverse(
            "accounts:accounts-api-v1:activation",
            kwargs={"token": "test-token"},
        ) == "/accounts/api/v1/activation/confirm/test-token/"
"""
