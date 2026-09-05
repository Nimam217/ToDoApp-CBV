"""import pytest

from django.urls import reverse, resolve

from task.views import (
    DashboardView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
)


@pytest.mark.django_db
class TestTaskURL:

    def test_dashboard_url(self):
        url = reverse("task:dashboard")

        assert url == "/task/dashboard/"
        assert resolve(url).func.view_class == DashboardView

    def test_detail_url(self, task):
        url = reverse(
            "task:detail",
            kwargs={"pk": task.pk},
        )

        assert url == f"/task/detail/{task.pk}/"
        assert resolve(url).func.view_class == TaskDetailView

    def test_create_url(self):
        url = reverse("task:create")

        assert url == "/task/create/"
        assert resolve(url).func.view_class == TaskCreateView

    def test_update_url(self, task):
        url = reverse(
            "task:update",
            kwargs={"pk": task.pk},
        )

        assert url == f"/task/update/{task.pk}/"
        assert resolve(url).func.view_class == TaskUpdateView

    def test_delete_url(self, task):
        url = reverse(
            "task:delete",
            kwargs={"pk": task.pk},
        )

        assert url == f"/task/delete/{task.pk}/"
        assert resolve(url).func.view_class == TaskDeleteView

"""
