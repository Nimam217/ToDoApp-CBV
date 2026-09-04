'''from django.urls import resolve, reverse

from accounts.api.v1.views import (
    ActivationView,
    ChangePasswordView,
    CustomAuthToken,
    CustomDiscardAuthToken,
    CustomObtainPairView,
    ProfileApiView,
    RegistrationApiView,
    ResendActivationEmail,
    ResetPasswordEmailView,
    ResetPasswordView,
)


class TestAccountsApiUrls:

    def test_registration_url(self):
        url = reverse("accounts:accounts-api-v1:registration")
        assert url == "/accounts/api/v1/registration/"
        assert resolve(url).func.view_class is RegistrationApiView

    def test_token_auth_url(self):
        url = reverse("accounts:accounts-api-v1:token_auth")
        assert url == "/accounts/api/v1/token-auth/create/"
        assert resolve(url).func.view_class is CustomAuthToken

    def test_discard_auth_token_url(self):
        url = reverse("accounts:accounts-api-v1:discard_auth_token")
        assert url == "/accounts/api/v1/token-auth/discard/"
        assert resolve(url).func.view_class is CustomDiscardAuthToken

    def test_profile_url(self):
        url = reverse("accounts:accounts-api-v1:profile")
        assert url == "/accounts/api/v1/profile/"
        assert resolve(url).func.view_class is ProfileApiView

    def test_token_obtain_pair_url(self):
        url = reverse("accounts:accounts-api-v1:token_obtain_pair")
        assert url == "/accounts/api/v1/jwt/create/"
        assert resolve(url).func.view_class is CustomObtainPairView

    def test_token_refresh_url(self):
        url = reverse("accounts:accounts-api-v1:token_refresh")
        assert url == "/accounts/api/v1/jwt/refresh/"

    def test_token_verify_url(self):
        url = reverse("accounts:accounts-api-v1:token_verify")
        assert url == "/accounts/api/v1/jwt/verify/"

    def test_change_password_url(self):
        url = reverse("accounts:accounts-api-v1:change_password")
        assert url == "/accounts/api/v1/change_password/"
        assert resolve(url).func.view_class is ChangePasswordView

    def test_reset_password_url(self):
        url = reverse("accounts:accounts-api-v1:reset_password")
        assert url == "/accounts/api/v1/reset_password/"
        assert resolve(url).func.view_class is ResetPasswordEmailView

    def test_reset_password_confirm_url(self):
        url = reverse(
            "accounts:accounts-api-v1:reset_password_confirm",
            kwargs={"token": "test-token"},
        )
        assert url == "/accounts/api/v1/reset_password/confirm/test-token/"
        assert resolve(url).func.view_class is ResetPasswordView

    def test_activation_resend_url(self):
        url = reverse("accounts:accounts-api-v1:activation_resend")
        assert url == "/accounts/api/v1/activation/resend/"
        assert resolve(url).func.view_class is ResendActivationEmail

    def test_activation_url(self):
        url = reverse(
            "accounts:accounts-api-v1:activation",
            kwargs={"token": "test-token"},
        )
        assert url == "/accounts/api/v1/activation/confirm/test-token/"
        assert resolve(url).func.view_class is ActivationView'''