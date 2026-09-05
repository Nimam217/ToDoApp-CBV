import pytest

from django.urls import reverse


from ...models import  Task
@pytest.mark.django_db
class TestDashboardView:

    def test_unauthenticated(self, client):
        url = reverse("task:dashboard")

        response = client.get(url)

        assert response.status_code == 302
        assert response.url.startswith(
            reverse("accounts:login")
        )

    def test_authenticated(self, client, user):
        client.force_login(user)

        url = reverse("task:dashboard")

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["status"] == "all"
        assert response.context["query"] == ""

    def test_all_tasks(self, client, user, task, completed_task):
        client.force_login(user)

        url = reverse("task:dashboard")

        response = client.get(url)

        assert response.status_code == 200

        assert response.context["total_tasks"] == 2
        assert response.context["pending_count"] == 1
        assert response.context["completed_count"] == 1

        assert task in response.context["pending_list"]
        assert completed_task in response.context["completed_list"]

    def test_only_pending_tasks(
        self,
        client,
        user,
        task,
        completed_task,
    ):
        client.force_login(user)

        url = reverse("task:dashboard")

        response = client.get(
            url,
            {"status": "pending"},
        )

        assert response.status_code == 200
        assert response.context["status"] == "pending"

        assert response.context["pending_list"].count() == 1
        assert response.context["completed_list"].count() == 0

        assert task in response.context["pending_list"]
        assert completed_task not in response.context["pending_list"]

    def test_only_completed_tasks(
        self,
        client,
        user,
        task,
        completed_task,
    ):
        client.force_login(user)

        url = reverse("task:dashboard")

        response = client.get(
            url,
            {"status": "completed"},
        )

        assert response.status_code == 200
        assert response.context["status"] == "completed"

        assert response.context["pending_list"].count() == 0
        assert response.context["completed_list"].count() == 1

        assert completed_task in response.context["completed_list"]
        assert task not in response.context["completed_list"]

    def test_search(self, client, user, task, completed_task):
        client.force_login(user)

        url = reverse("task:dashboard")

        response = client.get(
            url,
            {"q": "Test Task"},
        )

        assert response.status_code == 200
        assert response.context["query"] == "Test Task"

        assert task in response.context["pending_list"]
        assert completed_task not in response.context["completed_list"]

    def test_search_case_insensitive(
        self,
        client,
        user,
        task,
    ):
        client.force_login(user)

        url = reverse("task:dashboard")

        response = client.get(
            url,
            {"q": "test task"},
        )

        assert response.status_code == 200
        assert task in response.context["pending_list"]

    def test_search_with_no_result(
        self,
        client,
        user,
    ):
        client.force_login(user)

        url = reverse("task:dashboard")

        response = client.get(
            url,
            {"q": "does-not-exist"},
        )

        assert response.status_code == 200
        assert response.context["query"] == "does-not-exist"

        assert response.context["pending_list"].count() == 0
        assert response.context["completed_list"].count() == 0

    def test_user_can_only_see_own_tasks(
        self,
        client,
        user,
        task,
        another_task,
    ):
        client.force_login(user)

        url = reverse("task:dashboard")

        response = client.get(url)

        assert response.status_code == 200

        assert task in response.context["pending_list"]
        assert another_task not in response.context["pending_list"]

        assert response.context["total_tasks"] == 1

    def test_search_strips_whitespace(
        self,
        client,
        user,
        task,
    ):
        client.force_login(user)

        url = reverse("task:dashboard")

        response = client.get(
            url,
            {"q": "   Test Task   "},
        )

        assert response.status_code == 200
        assert response.context["query"] == "Test Task"
        assert task in response.context["pending_list"]


@pytest.mark.django_db
class TestTaskDetailView:

    def test_unauthenticated(self, client, task):
        url = reverse(
            "task:detail",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 302
        assert response.url.startswith(
            reverse("accounts:login")
        )

    def test_owner(self, client, user, task):
        client.force_login(user)

        url = reverse(
            "task:detail",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["object"] == task

    def test_other_user_cannot_access_task(
        self,
        client,
        another_user,
        task,
    ):
        client.force_login(another_user)

        url = reverse(
            "task:detail",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 404


@pytest.mark.django_db
class TestTaskCreateView:

    def test_unauthenticated(self, client):
        url = reverse("task:create")

        response = client.get(url)

        assert response.status_code == 302
        assert response.url.startswith(
            reverse("accounts:login")
        )

    def test_get(self, client, user):
        client.force_login(user)

        url = reverse("task:create")

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_create_task(self, client, user):
        client.force_login(user)

        url = reverse("task:create")

        response = client.post(
            url,
            {
                "title": "New Task",
                "description": "New task description",
            },
        )

        assert response.status_code == 302
        assert response.url == reverse("task:dashboard")

        created_task = Task.objects.get(
            title="New Task"
        )

        assert created_task.user == user
        assert created_task.description == "New task description"
        assert created_task.done is False


@pytest.mark.django_db
class TestTaskUpdateView:

    def test_unauthenticated(self, client, task):
        url = reverse(
            "task:update",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 302
        assert response.url.startswith(
            reverse("accounts:login")
        )

    def test_owner(self, client, user, task):
        client.force_login(user)

        url = reverse(
            "task:update",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["form"].instance == task

    def test_update_task(self, client, user, task):
        client.force_login(user)

        url = reverse(
            "task:update",
            kwargs={"pk": task.pk},
        )

        response = client.post(
            url,
            {
                "title": "Updated Task",
                "description": "Updated description",
            },
        )

        assert response.status_code == 302
        assert response.url == reverse("task:dashboard")

        task.refresh_from_db()

        assert task.title == "Updated Task"
        assert task.description == "Updated description"
        assert task.user == user

    def test_other_user_cannot_update_task(
        self,
        client,
        another_user,
        task,
    ):
        client.force_login(another_user)

        url = reverse(
            "task:update",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 404


@pytest.mark.django_db
class TestTaskDeleteView:

    def test_unauthenticated(self, client, task):
        url = reverse(
            "task:delete",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 302
        assert response.url.startswith(
            reverse("accounts:login")
        )

    def test_owner(self, client, user, task):
        client.force_login(user)

        url = reverse(
            "task:delete",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["object"] == task

    def test_delete_task(self, client, user, task):
        client.force_login(user)

        url = reverse(
            "task:delete",
            kwargs={"pk": task.pk},
        )

        response = client.post(url)

        assert response.status_code == 302
        assert response.url == reverse("task:dashboard")

        assert not Task.objects.filter(
            pk=task.pk
        ).exists()

    def test_other_user_cannot_delete_task(
        self,
        client,
        another_user,
        task,
    ):
        client.force_login(another_user)

        url = reverse(
            "task:delete",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 404
