import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestTaskAPIViews:

    def test_task_list_authenticated(self, api_client, user, task):
        api_client.force_authenticate(user=user)

        url = reverse("task:task_api_v1:task-api-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["total_task"] == 1
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == task.id

    def test_task_list_unauthenticated(self, api_client):
        url = reverse("task:task_api_v1:task-api-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_task_list_only_user_tasks(
        self,
        api_client,
        user,
        task,
        another_task,
    ):
        api_client.force_authenticate(user=user)

        url = reverse("task:task_api_v1:task-api-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["total_task"] == 1
        assert response.data["results"][0]["id"] == task.id

    def test_task_create_authenticated(self, api_client, user):
        api_client.force_authenticate(user=user)

        url = reverse("task:task_api_v1:task-api-list")

        data = {
            "title": "New Task",
            "description": "New task description",
            "done": False,
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "New Task"
        assert response.data["done"] is False
        assert response.data["user"] == user.id

        assert "description" not in response.data
        assert "desc" in response.data
        assert "task_url" in response.data

    def test_task_create_unauthenticated(self, api_client):
        url = reverse("task:task_api_v1:task-api-list")
        data = {
            "title": "New Task",
            "description": "New task description",
            "done": False,
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_task_retrieve_authenticated(self, api_client, user, task):
        api_client.force_authenticate(user=user)

        url = reverse(
            "task:task_api_v1:task-api-detail",
            kwargs={"pk": task.pk},
        )
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == task.id
        assert response.data["title"] == task.title
        assert response.data["description"] == task.description

    def test_task_retrieve_unauthenticated(self, api_client, task):
        url = reverse(
            "task:task_api_v1:task-api-detail",
            kwargs={"pk": task.pk},
        )
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_cannot_retrieve_another_users_task(
        self,
        api_client,
        user,
        another_task,
    ):
        api_client.force_authenticate(user=user)

        url = reverse(
            "task:task_api_v1:task-api-detail",
            kwargs={"pk": another_task.pk},
        )
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_task_update(self, api_client, user, task):
        api_client.force_authenticate(user=user)

        url = reverse(
            "task:task_api_v1:task-api-detail",
            kwargs={"pk": task.pk},
        )
        data = {
            "title": "Updated Task",
            "description": "Updated description",
            "done": True,
        }

        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated Task"
        assert response.data["description"] == "Updated description"
        assert response.data["done"] is True

        task.refresh_from_db()

        assert task.title == "Updated Task"
        assert task.description == "Updated description"
        assert task.done is True

    def test_task_partial_update(self, api_client, user, task):
        api_client.force_authenticate(user=user)

        url = reverse(
            "task:task_api_v1:task-api-detail",
            kwargs={"pk": task.pk},
        )
        data = {
            "title": "Partially Updated Task",
        }

        response = api_client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Partially Updated Task"

        task.refresh_from_db()

        assert task.title == "Partially Updated Task"

    def test_user_cannot_update_another_users_task(
        self,
        api_client,
        user,
        another_task,
    ):
        api_client.force_authenticate(user=user)

        url = reverse(
            "task:task_api_v1:task-api-detail",
            kwargs={"pk": another_task.pk},
        )
        data = {
            "title": "Hacked Task",
            "description": "Hacked description",
            "done": True,
        }

        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_task_delete(self, api_client, user, task):
        api_client.force_authenticate(user=user)

        url = reverse(
            "task:task_api_v1:task-api-detail",
            kwargs={"pk": task.pk},
        )
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not task.__class__.objects.filter(pk=task.pk).exists()

    def test_task_delete_unauthenticated(self, api_client, task):
        url = reverse(
            "task:task_api_v1:task-api-detail",
            kwargs={"pk": task.pk},
        )
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_cannot_delete_another_users_task(
        self,
        api_client,
        user,
        another_task,
    ):
        api_client.force_authenticate(user=user)

        url = reverse(
            "task:task_api_v1:task-api-detail",
            kwargs={"pk": another_task.pk},
        )
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_task_list_pagination(self, api_client, user, task):
        api_client.force_authenticate(user=user)

        # page_size = 2
        from task.models import Task

        Task.objects.create(
            title="Task 2",
            description="Task 2 description",
            user=user,
        )
        Task.objects.create(
            title="Task 3",
            description="Task 3 description",
            user=user,
        )

        url = reverse("task:task_api_v1:task-api-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["total_task"] == 3
        assert response.data["total_page"] == 2
        assert len(response.data["results"]) == 2
        assert "links" in response.data
        assert "next" in response.data["links"]
        assert "previous" in response.data["links"]

    def test_task_search(self, api_client, user):
        api_client.force_authenticate(user=user)

        from task.models import Task

        Task.objects.create(
            title="Learn Django",
            description="Study Django",
            user=user,
        )
        Task.objects.create(
            title="Learn DRF",
            description="Study DRF",
            user=user,
        )

        url = reverse("task:task_api_v1:task-api-list")
        response = api_client.get(url, {"search": "Django"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["total_task"] == 1
        assert response.data["results"][0]["title"] == "Learn Django"

    def test_task_ordering(self, api_client, user):
        api_client.force_authenticate(user=user)

        from task.models import Task

        first_task = Task.objects.create(
            title="First",
            description="First description",
            user=user,
            done=False,
        )
        second_task = Task.objects.create(
            title="Second",
            description="Second description",
            user=user,
            done=True,
        )

        url = reverse("task:task_api_v1:task-api-list")
        response = api_client.get(url, {"ordering": "done"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["id"] == first_task.id
        assert response.data["results"][1]["id"] == second_task.id
