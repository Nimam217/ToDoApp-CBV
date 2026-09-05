"""import pytest

from django.urls import resolve, reverse

from task.api.v1.views import TaskModelViewSet


@pytest.mark.django_db
class TestTaskAPIURL:

    def test_task_list_url(self):
        url = reverse("task:task_api_v1:task-api-list")

        assert url == "/task/api/v1/my-task/"
        assert resolve(url).func.cls == TaskModelViewSet

    def test_task_detail_url(self, task):
        url = reverse(
            "task:task_api_v1:task-api-detail",
            kwargs={"pk": task.pk},
        )

        assert url == f"/task/api/v1/my-task/{task.pk}/"
        assert resolve(url).func.cls == TaskModelViewSet
"""
