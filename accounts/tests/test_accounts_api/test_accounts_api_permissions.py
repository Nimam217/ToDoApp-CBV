"""from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory

from accounts.api.v1.permissions import IsVerifiedUser


class TestIsVerifiedUser:

    def test_verified_authenticated_user(self, verified_user):
        request = APIRequestFactory().get("/accounts/api/v1/profile/")
        request.user = verified_user

        permission = IsVerifiedUser()

        assert permission.has_permission(request, None) is True

    def test_unverified_authenticated_user(self, user):
        request = APIRequestFactory().get("/accounts/api/v1/profile/")
        request.user = user

        permission = IsVerifiedUser()

        assert permission.has_permission(request, None) is False

    def test_unauthenticated_user(self):
        request = APIRequestFactory().get("/accounts/api/v1/profile/")
        request.user = AnonymousUser()

        permission = IsVerifiedUser()

        assert permission.has_permission(request, None) is False
"""
