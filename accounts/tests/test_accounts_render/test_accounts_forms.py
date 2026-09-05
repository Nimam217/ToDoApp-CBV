'''import pytest
from django.contrib.auth import get_user_model

from accounts.forms import (
    CustomAuthenticationForm,
    CustomUserCreationForm,

)


User = get_user_model()


@pytest.mark.django_db
class TestCustomUserCreationForm:

    def test_form_fields(self):
        form = CustomUserCreationForm()

        assert "email" in form.fields
        assert "password1" in form.fields
        assert "password2" in form.fields

    def test_invalid_email(self):
        form = CustomUserCreationForm(
            data={
                "email": "invalid-email",
                "password1": "TestPassword123",
                "password2": "TestPassword123",
            }
        )

        assert not form.is_valid()
        assert "email" in form.errors

    def test_password_mismatch(self):
        form = CustomUserCreationForm(
            data={
                "email": "test@example.com",
                "password1": "TestPassword123",
                "password2": "DifferentPassword123",
            }
        )

        assert not form.is_valid()
        assert "password2" in form.errors

    def test_duplicate_email(self, user):
        form = CustomUserCreationForm(
            data={
                "email": user.email,
                "password1": "TestPassword123",
                "password2": "TestPassword123",
            }
        )

        assert not form.is_valid()
        assert "email" in form.errors

    def test_save_creates_user(self):
        form = CustomUserCreationForm(
            data={
                "email": "new@example.com",
                "password1": "TestPassword123",
                "password2": "TestPassword123",
            }
        )

        assert form.is_valid()

        user = form.save()

        assert user.email == "new@example.com"
        assert user.check_password("TestPassword123")


@pytest.mark.django_db
class TestCustomAuthenticationForm:

    def test_form_fields(self):
        form = CustomAuthenticationForm()

        assert "username" in form.fields
        assert "password" in form.fields

    def test_username_is_email_field(self):
        form = CustomAuthenticationForm()

        assert form.fields["username"].__class__.__name__ == "EmailField"

    def test_valid_login(self, verified_user):
        form = CustomAuthenticationForm(
            data={
                "username": verified_user.email,
                "password": "TestPassword123",
            }
        )

        assert form.is_valid(), form.errors
        assert form.get_user() == verified_user

    def test_unverified_user_cannot_login(self, user):
        form = CustomAuthenticationForm(
            data={
                "username": user.email,
                "password": "TestPassword123",
            }
        )

        assert not form.is_valid()

        error = form.non_field_errors().as_data()[0]

        assert error.code == "not-verified"
        assert str(error.message) == "Please verify your account."

    def test_invalid_password(self, verified_user):
        form = CustomAuthenticationForm(
            data={
                "username": verified_user.email,
                "password": "WrongPassword123",
            }
        )

        assert not form.is_valid()

    def test_nonexistent_user(self):
        form = CustomAuthenticationForm(
            data={
                "username": "notfound@example.com",
                "password": "TestPassword123",
            }
        )

        assert not form.is_valid()
'''