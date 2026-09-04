import jwt
import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch

from accounts.models import User


@pytest.mark.django_db
class TestRegistrationApiView:

    @patch("accounts.api.v1.views.send_activation_email")
    def test_registration(self, mock_send_activation_email, api_client):
        response = api_client.post(
            reverse("accounts:accounts-api-v1:registration"),
            {
                "email": "new@example.com",
                "password": "TestPassword123",
                "password_confirm": "TestPassword123",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {
            "email": "new@example.com",
            "detail": "Check your email box",
        }

        user = User.objects.get(email="new@example.com")

        assert user.is_verified is False
        assert user.check_password("TestPassword123")

        mock_send_activation_email.assert_called_once()

        called_user, called_token = (
            mock_send_activation_email.call_args.args
        )

        assert called_user == user
        assert isinstance(called_token, str)

    def test_registration_invalid_data(self, api_client):
        response = api_client.post(
            reverse("accounts:accounts-api-v1:registration"),
            {
                "email": "new@example.com",
                "password": "TestPassword123",
                "password_confirm": "DifferentPassword123",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_registration_duplicate_email(self, api_client, user):
        response = api_client.post(
            reverse("accounts:accounts-api-v1:registration"),
            {
                "email": user.email,
                "password": "TestPassword123",
                "password_confirm": "TestPassword123",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data


@pytest.mark.django_db
class TestCustomAuthToken:

    def test_valid_login(self, api_client, verified_user):
        response = api_client.post(
            reverse("accounts:accounts-api-v1:token_auth"),
            {
                "email": verified_user.email,
                "password": "TestPassword123",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.data
        assert response.data["user_id"] == verified_user.id
        assert response.data["email"] == verified_user.email

        token = Token.objects.get(user=verified_user)

        assert response.data["token"] == token.key

    def test_existing_token_is_reused(
        self,
        api_client,
        verified_user,
    ):
        token = Token.objects.create(user=verified_user)

        response = api_client.post(
            reverse("accounts:accounts-api-v1:token_auth"),
            {
                "email": verified_user.email,
                "password": "TestPassword123",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["token"] == token.key
        assert Token.objects.filter(user=verified_user).count() == 1

    def test_invalid_password(self, api_client, verified_user):
        response = api_client.post(
            reverse("accounts:accounts-api-v1:token_auth"),
            {
                "email": verified_user.email,
                "password": "WrongPassword123",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unverified_user(self, api_client, user):
        response = api_client.post(
            reverse("accounts:accounts-api-v1:token_auth"),
            {
                "email": user.email,
                "password": "TestPassword123",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Please verify your account." in str(response.data)


@pytest.mark.django_db
class TestCustomDiscardAuthToken:

    def test_authenticated(self, api_client, verified_user):
        token = Token.objects.create(user=verified_user)

        api_client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

        response = api_client.post(
            reverse("accounts:accounts-api-v1:discard_auth_token")
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Token.objects.filter(
            user=verified_user
        ).exists()

    def test_unauthenticated(self, api_client):
        response = api_client.post(
            reverse("accounts:accounts-api-v1:discard_auth_token")
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestProfileApiView:

    def test_get_profile(self, api_client, verified_user):
        api_client.force_authenticate(user=verified_user)

        response = api_client.get(
            reverse("accounts:accounts-api-v1:profile")
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == verified_user.email

    def test_update_profile(self, api_client, verified_user):
        api_client.force_authenticate(user=verified_user)

        response = api_client.put(
            reverse("accounts:accounts-api-v1:profile"),
            {
                "first_name": "Nima",
                "last_name": "Aghahadi",
                "description": "Updated profile",
            },
        )

        assert response.status_code == status.HTTP_200_OK

        verified_user.profile.refresh_from_db()

        assert verified_user.profile.first_name == "Nima"
        assert verified_user.profile.last_name == "Aghahadi"
        assert verified_user.profile.description == "Updated profile"

    def test_unauthenticated(self, api_client):
        response = api_client.get(
            reverse("accounts:accounts-api-v1:profile")
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unverified_user(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.get(
            reverse("accounts:accounts-api-v1:profile")
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestCustomObtainPairView:

    def test_valid_login(self, api_client, verified_user):
        response = api_client.post(
            reverse("accounts:accounts-api-v1:token_obtain_pair"),
            {
                "email": verified_user.email,
                "password": "TestPassword123",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["user_id"] == verified_user.id
        assert response.data["user"]["email"] == verified_user.email

    def test_unverified_user(self, api_client, user):
        response = api_client.post(
            reverse("accounts:accounts-api-v1:token_obtain_pair"),
            {
                "email": user.email,
                "password": "TestPassword123",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_password(self, api_client, verified_user):
        response = api_client.post(
            reverse("accounts:accounts-api-v1:token_obtain_pair"),
            {
                "email": verified_user.email,
                "password": "WrongPassword123",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestChangePasswordView:

    def test_change_password(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.put(
            reverse("accounts:accounts-api-v1:change_password"),
            {
                "old_password": "TestPassword123",
                "new_password1": "NewPassword123",
                "new_password2": "NewPassword123",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "success"
        assert response.data["code"] == status.HTTP_200_OK
        assert response.data["message"] == "Password updated successfully"

        user.refresh_from_db()

        assert user.check_password("NewPassword123")

    def test_wrong_old_password(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.put(
            reverse("accounts:accounts-api-v1:change_password"),
            {
                "old_password": "WrongPassword123",
                "new_password1": "NewPassword123",
                "new_password2": "NewPassword123",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["old_password"] == ["wrong password"]

    def test_password_mismatch(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.put(
            reverse("accounts:accounts-api-v1:change_password"),
            {
                "old_password": "TestPassword123",
                "new_password1": "NewPassword123",
                "new_password2": "DifferentPassword123",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "new_password1" in response.data

    def test_unauthenticated(self, api_client):
        response = api_client.put(
            reverse("accounts:accounts-api-v1:change_password"),
            {
                "old_password": "TestPassword123",
                "new_password1": "NewPassword123",
                "new_password2": "NewPassword123",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestResetPasswordEmailView:

    @patch("accounts.api.v1.views.send_reset_password_email")
    def test_valid_email(
        self,
        mock_send_reset_password_email,
        api_client,
        user,
    ):
        response = api_client.post(
            reverse("accounts:accounts-api-v1:reset_password"),
            {"email": user.email},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "email": "Successfully send"
        }

        mock_send_reset_password_email.assert_called_once()

        called_user, called_token = (
            mock_send_reset_password_email.call_args.args
        )

        assert called_user == user
        assert isinstance(called_token, str)

    def test_nonexistent_email(self, api_client):
        response = api_client.post(
            reverse("accounts:accounts-api-v1:reset_password"),
            {"email": "notfound@example.com"},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data


@pytest.mark.django_db
class TestResetPasswordView:

    def test_valid_token(self, api_client, verified_user):
        refresh = RefreshToken.for_user(verified_user)
        token = str(refresh.access_token)

        response = api_client.post(
            reverse(
                "accounts:accounts-api-v1:reset_password_confirm",
                kwargs={"token": token},
            ),
            {
                "new_password1": "NewPassword123",
                "new_password2": "NewPassword123",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "password": "Successfully reset your password"
        }

        verified_user.refresh_from_db()

        assert verified_user.check_password(
            "NewPassword123"
        )

    def test_unverified_user(self, api_client, user):
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        response = api_client.post(
            reverse(
                "accounts:accounts-api-v1:reset_password_confirm",
                kwargs={"token": token},
            ),
            {
                "new_password1": "NewPassword123",
                "new_password2": "NewPassword123",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "User is not verified"

    def test_invalid_token(self, api_client):
        response = api_client.post(
            reverse(
                "accounts:accounts-api-v1:reset_password_confirm",
                kwargs={"token": "invalid-token"},
            ),
            {
                "new_password1": "NewPassword123",
                "new_password2": "NewPassword123",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid Token"


@pytest.mark.django_db
class TestActivationView:

    def test_activate_user(self, api_client, user):
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        response = api_client.get(
            reverse(
                "accounts:accounts-api-v1:activation",
                kwargs={"token": token},
            )
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "email": "Successfully activated"
        }

        user.refresh_from_db()

        assert user.is_verified is True

    def test_already_verified_user(
        self,
        api_client,
        verified_user,
    ):
        refresh = RefreshToken.for_user(verified_user)
        token = str(refresh.access_token)

        response = api_client.get(
            reverse(
                "accounts:accounts-api-v1:activation",
                kwargs={"token": token},
            )
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == (
            "User has already been verified"
        )

    def test_invalid_token(self, api_client):
        response = api_client.get(
            reverse(
                "accounts:accounts-api-v1:activation",
                kwargs={"token": "invalid-token"},
            )
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid Token"


@pytest.mark.django_db
class TestResendActivationEmail:

    @patch("accounts.api.v1.views.send_activation_email")
    def test_resend_activation_email(
        self,
        mock_send_activation_email,
        api_client,
        user,
    ):
        api_client.force_authenticate(user=user)

        response = api_client.post(
            reverse(
                "accounts:accounts-api-v1:activation_resend"
            ),
            {"email": user.email},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "detail": "email has been sent successfully"
        }

        mock_send_activation_email.assert_called_once()

        called_user, called_token = (
            mock_send_activation_email.call_args.args
        )

        assert called_user == user
        assert isinstance(called_token, str)

    def test_unauthenticated(self, api_client, user):
        response = api_client.post(
            reverse(
                "accounts:accounts-api-v1:activation_resend"
            ),
            {"email": user.email},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_nonexistent_user(
        self,
        api_client,
        user,
    ):
        api_client.force_authenticate(user=user)

        response = api_client.post(
            reverse(
                "accounts:accounts-api-v1:activation_resend"
            ),
            {"email": "notfound@example.com"},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data