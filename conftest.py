import pytest

from django.contrib.auth import get_user_model
from django.test import RequestFactory

from rest_framework.test import APIClient

from task.models import Task


User = get_user_model()


# =========================
# Users
# =========================

@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="user@example.com",
        password="TestPassword123",
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        email="another@example.com",
        password="TestPassword123",
    )


@pytest.fixture
def verified_user(db):
    return User.objects.create_user(
        email="verified@example.com",
        password="TestPassword123",
        is_verified=True,
    )


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(
        email="staff@example.com",
        password="TestPassword123",
        is_staff=True,
    )


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(
        email="admin@example.com",
        password="AdminPassword123",
    )


# =========================
# Profiles
# =========================

@pytest.fixture
def profile(user):
    return user.profile


@pytest.fixture
def another_profile(another_user):
    return another_user.profile


# =========================
# Tasks
# =========================

@pytest.fixture
def task(db, user):
    return Task.objects.create(
        title="Test Task",
        description="Test task description",
        user=user,
        done=False,
    )


@pytest.fixture
def completed_task(db, user):
    return Task.objects.create(
        title="Completed Task",
        description="Completed task description",
        user=user,
        done=True,
    )


@pytest.fixture
def another_task(db, another_user):
    return Task.objects.create(
        title="Another Task",
        description="Another task description",
        user=another_user,
        done=False,
    )


# =========================
# Django RequestFactory
# =========================

@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def list_request(request_factory):
    request = request_factory.get("/task/api/v1/")
    request.parser_context = {
        "kwargs": {}
    }

    return request


@pytest.fixture
def detail_request(request_factory, task):
    request = request_factory.get(
        f"/task/api/v1/{task.pk}/"
    )
    request.parser_context = {
        "kwargs": {
            "pk": task.pk,
        }
    }

    return request


# =========================
# DRF APIClient
# =========================

@pytest.fixture
def api_client():
    return APIClient()