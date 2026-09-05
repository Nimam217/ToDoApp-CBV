import pytest
from django.contrib.auth import get_user_model

from accounts.models import Profile


User = get_user_model()


@pytest.mark.django_db
class TestUserModel:

    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="TestPassword123",
        )

        assert user.email == "test@example.com"
        assert user.check_password("TestPassword123")
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.is_verified is False

    def test_create_user_normalizes_email(self):
        user = User.objects.create_user(
            email="TEST@EXAMPLE.COM",
            password="TestPassword123",
        )

        assert user.email == "TEST@example.com"

    def test_create_user_without_email(self):
        with pytest.raises(ValueError, match="The Email must be set"):
            User.objects.create_user(
                email="",
                password="TestPassword123",
            )

    def test_user_str(self, user):
        assert str(user) == user.email


@pytest.mark.django_db
class TestSuperUser:

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="admin@example.com",
            password="AdminPassword123",
        )

        assert user.email == "admin@example.com"
        assert user.check_password("AdminPassword123")
        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.is_active is True
        assert user.is_verified is True

    def test_create_superuser_invalid_staff(self):
        with pytest.raises(
            ValueError,
            match="Superuser must have is_staff=True.",
        ):
            User.objects.create_superuser(
                email="admin@example.com",
                password="AdminPassword123",
                is_staff=False,
            )

    def test_create_superuser_invalid_superuser(self):
        with pytest.raises(
            ValueError,
            match="Superuser must have is_superuser=True.",
        ):
            User.objects.create_superuser(
                email="admin@example.com",
                password="AdminPassword123",
                is_superuser=False,
            )


@pytest.mark.django_db
class TestProfileModel:

    def test_profile_created_automatically(self, user):
        assert Profile.objects.filter(user=user).exists()

    def test_profile_belongs_to_user(self, user):
        profile = user.profile

        assert profile.user == user

    def test_profile_str(self, user):
        profile = user.profile

        assert str(profile) == user.email

    def test_profile_one_to_one(self, user):
        profile = user.profile

        assert profile.user_id == user.id
        assert Profile.objects.filter(user=user).count() == 1
