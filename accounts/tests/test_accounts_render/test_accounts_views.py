import jwt
import pytest

from unittest.mock import patch

from django.contrib.auth import get_user_model
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
    ResendActivationEmailView,
    ActivationConfirmView,
)

User = get_user_model()


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

    @patch("accounts.views.send_web_activation_email_task.apply_async")
    def test_register_success(
        self,
        mock_apply_async,
        client,
    ):
        response = client.post(
            reverse("accounts:register"),
            {
                "email": "newuser@example.com",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
            },
        )

        assert response.status_code == 302
        assert response.url == reverse("core:home")

        user = User.objects.get(email="newuser@example.com")

        assert user.is_verified is False

        mock_apply_async.assert_called_once()

        call_kwargs = mock_apply_async.call_args.kwargs

        assert call_kwargs["expires"] == 60
        assert call_kwargs["retry"] is True

        assert call_kwargs["args"][1] == user.id

        assert call_kwargs["retry_policy"] == {
            "max_retries": 3,
            "interval_start": 1,
            "interval_step": 2,
            "interval_max": 10,
        }


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

    def test_login_success(
        self,
        client,
        verified_user,
    ):
        response = client.post(
            reverse("accounts:login"),
            {
                "username": verified_user.email,
                "password": "TestPassword123",
            },
        )

        assert response.status_code == 302
        assert response.url == reverse("core:home")

        assert "_auth_user_id" in client.session


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

    def test_authenticated(
        self,
        client,
        verified_user,
    ):
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

    def test_authenticated(
        self,
        client,
        verified_user,
    ):
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

    def test_unauthenticated(
        self,
        client,
        user,
    ):
        url = reverse(
            "accounts:profile",
            kwargs={
                "pk": user.profile.pk,
            },
        )

        response = client.get(url)

        assert response.status_code == 302
        assert response.url.startswith(reverse("accounts:login"))

    def test_unverified_user(
        self,
        client,
        user,
    ):
        client.force_login(user)

        url = reverse(
            "accounts:profile",
            kwargs={
                "pk": user.profile.pk,
            },
        )

        response = client.get(url)

        assert response.status_code == 302
        assert response.url == reverse("core:home")

    def test_authenticated_owner(
        self,
        client,
        verified_user,
    ):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile",
            kwargs={
                "pk": verified_user.profile.pk,
            },
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
            kwargs={
                "pk": another_user.profile.pk,
            },
        )

        response = client.get(url)

        assert response.status_code == 404

    def test_view_class(
        self,
        client,
        verified_user,
    ):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile",
            kwargs={
                "pk": verified_user.profile.pk,
            },
        )

        response = client.get(url)

        assert response.resolver_match.func.view_class is ProfileView


# ============================================================
# Profile Update
# ============================================================


@pytest.mark.django_db
class TestProfileUpdateView:

    def test_unauthenticated(
        self,
        client,
        user,
    ):
        url = reverse(
            "accounts:profile_edit",
            kwargs={
                "pk": user.profile.pk,
            },
        )

        response = client.get(url)

        assert response.status_code == 302
        assert response.url.startswith(reverse("accounts:login"))

    def test_unverified_user(
        self,
        client,
        user,
    ):
        client.force_login(user)

        url = reverse(
            "accounts:profile_edit",
            kwargs={
                "pk": user.profile.pk,
            },
        )

        response = client.get(url)

        assert response.status_code == 302
        assert response.url == reverse("core:home")

    def test_authenticated_owner(
        self,
        client,
        verified_user,
    ):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile_edit",
            kwargs={
                "pk": verified_user.profile.pk,
            },
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
            kwargs={
                "pk": another_user.profile.pk,
            },
        )

        response = client.get(url)

        assert response.status_code == 404

    def test_view_class(
        self,
        client,
        verified_user,
    ):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile_edit",
            kwargs={
                "pk": verified_user.profile.pk,
            },
        )

        response = client.get(url)

        assert response.resolver_match.func.view_class is ProfileUpdateView


# ============================================================
# Resend Activation Email
# ============================================================


@pytest.mark.django_db
class TestResendActivationEmailView:

    def test_get(self, client):
        response = client.get(reverse("accounts:resend_activation"))

        assert response.status_code == 200
        assert "form" in response.context

    def test_view_class(self, client):
        response = client.get(reverse("accounts:resend_activation"))

        assert (
            response.resolver_match.func.view_class
            is ResendActivationEmailView
        )

    @patch("accounts.views.send_web_activation_email_task.apply_async")
    def test_unverified_user(
        self,
        mock_apply_async,
        client,
        user,
    ):
        response = client.post(
            reverse("accounts:resend_activation"),
            {
                "email": user.email,
            },
        )

        assert response.status_code == 302
        assert response.url == reverse("accounts:login")

        mock_apply_async.assert_called_once()

        call_kwargs = mock_apply_async.call_args.kwargs

        assert call_kwargs["args"][1] == user.id
        assert call_kwargs["expires"] == 60
        assert call_kwargs["retry"] is True

    @patch("accounts.views.send_web_activation_email_task.apply_async")
    def test_verified_user(
        self,
        mock_apply_async,
        client,
        verified_user,
    ):
        response = client.post(
            reverse("accounts:resend_activation"),
            {
                "email": verified_user.email,
            },
        )

        assert response.status_code == 302
        assert response.url == reverse("accounts:login")

        mock_apply_async.assert_not_called()

    @patch("accounts.views.send_web_activation_email_task.apply_async")
    def test_nonexistent_user(
        self,
        mock_apply_async,
        client,
    ):
        response = client.post(
            reverse("accounts:resend_activation"),
            {
                "email": "doesnotexist@example.com",
            },
        )

        assert response.status_code == 302
        assert response.url == reverse("accounts:login")

        mock_apply_async.assert_not_called()


# ============================================================
# Activation Confirm
# ============================================================


@pytest.mark.django_db
class TestActivationConfirmView:

    def test_view_class(self, client):
        url = reverse(
            "accounts:activation_confirm",
            kwargs={
                "token": "invalid-token",
            },
        )

        response = client.get(url)

        assert response.resolver_match.func.view_class is ActivationConfirmView

    def test_invalid_token(self, client):
        url = reverse(
            "accounts:activation_confirm",
            kwargs={
                "token": "invalid-token",
            },
        )

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["status"] == "invalid"

    def test_already_verified_user(
        self,
        client,
        verified_user,
    ):
        token = jwt.encode(
            {
                "user_id": verified_user.id,
            },
            "test-secret",
            algorithm="HS256",
        )

        with patch(
            "accounts.views.settings.SECRET_KEY",
            "test-secret",
        ):
            url = reverse(
                "accounts:activation_confirm",
                kwargs={
                    "token": token,
                },
            )

            response = client.get(url)

        assert response.status_code == 200
        assert response.context["status"] == "already_verified"

    def test_activate_unverified_user(
        self,
        client,
        user,
    ):
        token = jwt.encode(
            {
                "user_id": user.id,
            },
            "test-secret",
            algorithm="HS256",
        )

        with patch(
            "accounts.views.settings.SECRET_KEY",
            "test-secret",
        ):
            url = reverse(
                "accounts:activation_confirm",
                kwargs={
                    "token": token,
                },
            )

            response = client.get(url)

        assert response.status_code == 200
        assert response.context["status"] == "success"

        user.refresh_from_db()

        assert user.is_verified is True

    def test_nonexistent_user(
        self,
        client,
    ):
        token = jwt.encode(
            {
                "user_id": 999999,
            },
            "test-secret",
            algorithm="HS256",
        )

        with patch(
            "accounts.views.settings.SECRET_KEY",
            "test-secret",
        ):
            url = reverse(
                "accounts:activation_confirm",
                kwargs={
                    "token": token,
                },
            )

            response = client.get(url)

        assert response.status_code == 200
        assert response.context["status"] == "invalid"

    def test_expired_token(
        self,
        client,
    ):
        import datetime

        token = jwt.encode(
            {
                "user_id": 1,
                "exp": datetime.datetime.now(datetime.timezone.utc)
                - datetime.timedelta(seconds=10),
            },
            "test-secret",
            algorithm="HS256",
        )

        with patch(
            "accounts.views.settings.SECRET_KEY",
            "test-secret",
        ):
            url = reverse(
                "accounts:activation_confirm",
                kwargs={
                    "token": token,
                },
            )

            response = client.get(url)

        assert response.status_code == 200
        assert response.context["status"] == "expired"
