"""import pytest

from django.urls import reverse

from task.models import Task


@pytest.mark.django_db
class TestHomeView:

    def test_home_for_anonymous_user(self, client):
        response = client.get(reverse("core:home"))

        assert response.status_code == 200
        assert "total_tasks" not in response.context
        assert "pending_count" not in response.context
        assert "completed_count" not in response.context
        assert "recent_tasks" not in response.context

    def test_home_for_authenticated_user(
        self,
        client,
        user,
    ):
        client.force_login(user)

        response = client.get(reverse("core:home"))

        assert response.status_code == 200
        assert response.context["total_tasks"] == 0
        assert response.context["pending_count"] == 0
        assert response.context["completed_count"] == 0
        assert list(response.context["recent_tasks"]) == []

    def test_home_task_counts(
        self,
        client,
        user,
    ):
        client.force_login(user)

        Task.objects.create(
            title="Pending task",
            description="Pending description",
            user=user,
            done=False,
        )

        Task.objects.create(
            title="Completed task",
            description="Completed description",
            user=user,
            done=True,
        )

        response = client.get(reverse("core:home"))

        assert response.context["total_tasks"] == 2
        assert response.context["pending_count"] == 1
        assert response.context["completed_count"] == 1

    def test_home_shows_only_user_tasks(
        self,
        client,
        user,
        another_user,
    ):
        client.force_login(user)

        Task.objects.create(
            title="My task",
            description="My description",
            user=user,
        )

        Task.objects.create(
            title="Another user's task",
            description="Another description",
            user=another_user,
        )

        response = client.get(reverse("core:home"))

        assert response.context["total_tasks"] == 1
        assert response.context["pending_count"] == 1
        assert response.context["completed_count"] == 0

    def test_home_recent_tasks_contains_only_three_latest(
        self,
        client,
        user,
    ):
        client.force_login(user)

        for i in range(5):
            Task.objects.create(
                title=f"Task {i}",
                description=f"Description {i}",
                user=user,
            )

        response = client.get(reverse("core:home"))

        recent_tasks = response.context["recent_tasks"]

        assert len(recent_tasks) == 3
        assert recent_tasks[0].created_at >= recent_tasks[1].created_at
        assert recent_tasks[1].created_at >= recent_tasks[2].created_at"""
