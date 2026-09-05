'''import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from accounts.api.v1.serializers import (
    RegisterSerializer,
    AuthTokenSerializer,
    ProfileSerializer,
    TokenObtainPairViewSerializer,
    ChangePasswordSerializer,
    ResendActivationSerializer,
    ResetPasswordEmailSerializer,
    ResetPasswordSerializer,
)

User = get_user_model()


@pytest.mark.django_db
class TestRegisterSerializer:

    def test_valid_data(self):
        serializer = RegisterSerializer(
            data={
                "email": "new@example.com",
                "password": "TestPassword123",
                "password_confirm": "TestPassword123",
            }
        )

        assert serializer.is_valid()
        user = serializer.save()

        assert user.email == "new@example.com"
        assert user.check_password("TestPassword123")
        assert user.is_verified is False

    def test_password_mismatch(self):
        serializer = RegisterSerializer(
            data={
                "email": "new@example.com",
                "password": "TestPassword123",
                "password_confirm": "DifferentPassword123",
            }
        )

        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    def test_weak_password(self):
        serializer = RegisterSerializer(
            data={
                "email": "new@example.com",
                "password": "123",
                "password_confirm": "123",
            }
        )

        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_duplicate_email(self, user):
        serializer = RegisterSerializer(
            data={
                "email": user.email,
                "password": "TestPassword123",
                "password_confirm": "TestPassword123",
            }
        )

        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_password_is_write_only(self):
        serializer = RegisterSerializer()

        assert serializer.fields["password"].write_only is True


@pytest.mark.django_db
class TestAuthTokenSerializer:

    def test_valid_credentials(self, verified_user):
        serializer = AuthTokenSerializer(
            data={
                "email": verified_user.email,
                "password": "TestPassword123",
            }
        )

        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data["user"] == verified_user

    def test_invalid_password(self, verified_user):
        serializer = AuthTokenSerializer(
            data={
                "email": verified_user.email,
                "password": "WrongPassword123",
            }
        )

        assert not serializer.is_valid()

    def test_unverified_user(self, user):
        serializer = AuthTokenSerializer(
            data={
                "email": user.email,
                "password": "TestPassword123",
            }
        )

        assert not serializer.is_valid()

        error = serializer.errors["non_field_errors"][0]

        assert error == "Please verify your account."

    def test_missing_email(self):
        serializer = AuthTokenSerializer(
            data={
                "password": "TestPassword123",
            }
        )

        assert not serializer.is_valid()

    def test_missing_password(self):
        serializer = AuthTokenSerializer(
            data={
                "email": "user@example.com",
            }
        )

        assert not serializer.is_valid()


@pytest.mark.django_db
class TestProfileSerializer:

    def test_serialization(self, profile):
        serializer = ProfileSerializer(profile)

        assert serializer.data["email"] == profile.user.email
        assert serializer.data["first_name"] == profile.first_name
        assert serializer.data["last_name"] == profile.last_name
        assert serializer.data["description"] == profile.description

    def test_email_is_read_only(self):
        serializer = ProfileSerializer()

        assert serializer.fields["email"].read_only is True

    def test_update(self, profile):
        serializer = ProfileSerializer(
            instance=profile,
            data={
                "first_name": "John",
                "last_name": "Doe",
                "description": "Updated description",
            },
            partial=True,
        )

        assert serializer.is_valid(), serializer.errors

        updated_profile = serializer.save()

        assert updated_profile.first_name == "John"
        assert updated_profile.last_name == "Doe"
        assert updated_profile.description == "Updated description"


@pytest.mark.django_db
class TestTokenObtainPairViewSerializer:

    def test_verified_user(self, verified_user):
        serializer = TokenObtainPairViewSerializer(
            data={
                "email": verified_user.email,
                "password": "TestPassword123",
            }
        )

        assert serializer.is_valid(), serializer.errors
        assert "access" in serializer.validated_data
        assert "refresh" in serializer.validated_data
        assert serializer.validated_data["user"]["user_id"] == verified_user.id
        assert (
            serializer.validated_data["user"]["email"] == verified_user.email
        )

    def test_unverified_user(self, user):
        serializer = TokenObtainPairViewSerializer(
            data={
                "email": user.email,
                "password": "TestPassword123",
            }
        )

        assert not serializer.is_valid()
        assert "Please verify your account." in str(serializer.errors)

    def test_invalid_password(self, verified_user):
        serializer = TokenObtainPairViewSerializer(
            data={
                "email": verified_user.email,
                "password": "WrongPassword123",
            }
        )

        with pytest.raises(AuthenticationFailed):
            serializer.is_valid()


@pytest.mark.django_db
class TestChangePasswordSerializer:

    def test_valid_data(self, user):
        serializer = ChangePasswordSerializer(
            instance=user,
            data={
                "old_password": "TestPassword123",
                "new_password1": "NewPassword123",
                "new_password2": "NewPassword123",
            },
        )

        assert serializer.is_valid(), serializer.errors

    def test_password_mismatch(self, user):
        serializer = ChangePasswordSerializer(
            instance=user,
            data={
                "old_password": "TestPassword123",
                "new_password1": "NewPassword123",
                "new_password2": "DifferentPassword123",
            },
        )

        assert not serializer.is_valid()
        assert "new_password1" in serializer.errors

    def test_weak_password(self, user):
        serializer = ChangePasswordSerializer(
            instance=user,
            data={
                "old_password": "TestPassword123",
                "new_password1": "123",
                "new_password2": "123",
            },
        )

        assert not serializer.is_valid()
        assert "new_password1" in serializer.errors


@pytest.mark.django_db
class TestResendActivationSerializer:

    def test_valid_email(self, user):
        serializer = ResendActivationSerializer(data={"email": user.email})

        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data["user"] == user

    def test_nonexistent_email(self):
        serializer = ResendActivationSerializer(
            data={"email": "notfound@example.com"}
        )

        assert not serializer.is_valid()
        assert "email" in serializer.errors


@pytest.mark.django_db
class TestResetPasswordEmailSerializer:

    def test_valid_email(self, user):
        serializer = ResetPasswordEmailSerializer(data={"email": user.email})

        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data["user"] == user

    def test_nonexistent_email(self):
        serializer = ResetPasswordEmailSerializer(
            data={"email": "notfound@example.com"}
        )

        assert not serializer.is_valid()
        assert "email" in serializer.errors


class TestResetPasswordSerializer:

    def test_valid_data(self):
        serializer = ResetPasswordSerializer(
            data={
                "new_password1": "NewPassword123",
                "new_password2": "NewPassword123",
            }
        )

        assert serializer.is_valid(), serializer.errors

    def test_password_mismatch(self):
        serializer = ResetPasswordSerializer(
            data={
                "new_password1": "NewPassword123",
                "new_password2": "DifferentPassword123",
            }
        )

        assert not serializer.is_valid()
        assert "new_password1" in serializer.errors

    def test_weak_password(self):
        serializer = ResetPasswordSerializer(
            data={
                "new_password1": "123",
                "new_password2": "123",
            }
        )

        assert not serializer.is_valid()
        assert "new_password1" in serializer.errors
'''