'''import pytest

from django.urls import reverse

from task.models import Task


@pytest.mark.django_db
class TestDashboardView:

    def test_dashboard_requires_login(self, client):
        response = client.get(reverse("task:dashboard"))

        assert response.status_code == 302

    def test_dashboard_status_code(self, client, user):
        client.force_login(user)

        response = client.get(reverse("task:dashboard"))

        assert response.status_code == 200

    def test_dashboard_template(self, client, user):
        client.force_login(user)

        response = client.get(reverse("task:dashboard"))

        assert "task/dashboard.html" in [
            template.name
            for template in response.templates
        ]

    def test_dashboard_shows_only_user_tasks(
        self,
        client,
        user,
        another_user,
    ):
        client.force_login(user)

        user_task = Task.objects.create(
            title="My Task",
            description="My description",
            user=user,
        )

        Task.objects.create(
            title="Another User Task",
            description="Another description",
            user=another_user,
        )

        response = client.get(reverse("task:dashboard"))

        assert user_task in response.context["pending_list"]
        assert response.context["pending_list"].count() == 1

    def test_dashboard_statistics(
        self,
        client,
        user,
    ):
        client.force_login(user)

        Task.objects.create(
            title="Pending 1",
            description="Description",
            user=user,
            done=False,
        )

        Task.objects.create(
            title="Pending 2",
            description="Description",
            user=user,
            done=False,
        )

        Task.objects.create(
            title="Completed",
            description="Description",
            user=user,
            done=True,
        )

        response = client.get(reverse("task:dashboard"))

        assert response.context["total_tasks"] == 3
        assert response.context["pending_count"] == 2
        assert response.context["completed_count"] == 1

    def test_dashboard_search(
        self,
        client,
        user,
    ):
        client.force_login(user)

        matching_task = Task.objects.create(
            title="Learn Django",
            description="Description",
            user=user,
        )

        Task.objects.create(
            title="Learn Python",
            description="Description",
            user=user,
        )

        response = client.get(
            reverse("task:dashboard"),
            {"q": "Django"},
        )

        assert matching_task in response.context["pending_list"]
        assert response.context["pending_list"].count() == 1
        assert response.context["query"] == "Django"

    def test_dashboard_pending_status(
        self,
        client,
        user,
    ):
        client.force_login(user)

        pending_task = Task.objects.create(
            title="Pending",
            description="Description",
            user=user,
            done=False,
        )

        completed_task = Task.objects.create(
            title="Completed",
            description="Description",
            user=user,
            done=True,
        )

        response = client.get(
            reverse("task:dashboard"),
            {"status": "pending"},
        )

        assert response.context["status"] == "pending"
        assert pending_task in response.context["pending_list"]
        assert completed_task not in response.context["pending_list"]
        assert response.context["completed_list"].count() == 0

    def test_dashboard_completed_status(
        self,
        client,
        user,
    ):
        client.force_login(user)

        Task.objects.create(
            title="Pending",
            description="Description",
            user=user,
            done=False,
        )

        completed_task = Task.objects.create(
            title="Completed",
            description="Description",
            user=user,
            done=True,
        )

        response = client.get(
            reverse("task:dashboard"),
            {"status": "completed"},
        )

        assert response.context["status"] == "completed"
        assert completed_task in response.context["completed_list"]
        assert response.context["pending_list"].count() == 0


@pytest.mark.django_db
class TestTaskDetailView:

    def test_detail_requires_login(self, client, task):
        response = client.get(
            reverse("task:detail", kwargs={"pk": task.pk})
        )

        assert response.status_code == 302

    def test_detail_status_code(self, client, user, task):
        client.force_login(user)

        response = client.get(
            reverse("task:detail", kwargs={"pk": task.pk})
        )

        assert response.status_code == 200

    def test_detail_template(self, client, user, task):
        client.force_login(user)

        response = client.get(
            reverse("task:detail", kwargs={"pk": task.pk})
        )

        assert "task/detail.html" in [
            template.name
            for template in response.templates
        ]

    def test_user_cannot_access_another_users_task(
        self,
        client,
        user,
        another_task,
    ):
        client.force_login(user)

        response = client.get(
            reverse(
                "task:detail",
                kwargs={"pk": another_task.pk},
            )
        )

        assert response.status_code == 404


@pytest.mark.django_db
class TestTaskCreateView:

    def test_create_requires_login(self, client):
        response = client.get(
            reverse("task:create")
        )

        assert response.status_code == 302

    def test_create_status_code(self, client, user):
        client.force_login(user)

        response = client.get(
            reverse("task:create")
        )

        assert response.status_code == 200

    def test_create_template(self, client, user):
        client.force_login(user)

        response = client.get(
            reverse("task:create")
        )

        assert "task/create.html" in [
            template.name
            for template in response.templates
        ]

    def test_create_task(
        self,
        client,
        user,
    ):
        client.force_login(user)

        response = client.post(
            reverse("task:create"),
            {
                "title": "New Task",
                "description": "New description",
                "done": False,
            },
        )

        task = Task.objects.get(title="New Task")

        assert response.status_code == 302
        assert task.user == user
        assert task.description == "New description"
        assert task.done is False

    def test_create_redirects_to_dashboard(
        self,
        client,
        user,
    ):
        client.force_login(user)

        response = client.post(
            reverse("task:create"),
            {
                "title": "New Task",
                "description": "Description",
                "done": False,
            },
        )

        assert response.url == reverse("task:dashboard")


@pytest.mark.django_db
class TestTaskUpdateView:

    def test_update_requires_login(self, client, task):
        response = client.get(
            reverse(
                "task:update",
                kwargs={"pk": task.pk},
            )
        )

        assert response.status_code == 302

    def test_update_status_code(self, client, user, task):
        client.force_login(user)

        response = client.get(
            reverse(
                "task:update",
                kwargs={"pk": task.pk},
            )
        )

        assert response.status_code == 200

    def test_update_task(self, client, user, task):
        client.force_login(user)

        response = client.post(
            reverse(
                "task:update",
                kwargs={"pk": task.pk},
            ),
            {
                "title": "Updated Task",
                "description": "Updated description",
                "done": True,
            },
        )

        task.refresh_from_db()

        assert response.status_code == 302
        assert task.title == "Updated Task"
        assert task.description == "Updated description"
        assert task.done is True

    def test_user_cannot_update_another_users_task(
        self,
        client,
        user,
        another_task,
    ):
        client.force_login(user)

        response = client.post(
            reverse(
                "task:update",
                kwargs={"pk": another_task.pk},
            ),
            {
                "title": "Hacked Task",
                "description": "Hacked description",
                "done": True,
            },
        )

        assert response.status_code == 404

        another_task.refresh_from_db()

        assert another_task.title == "Another Task"


@pytest.mark.django_db
class TestTaskDeleteView:

    def test_delete_requires_login(self, client, task):
        response = client.get(
            reverse(
                "task:delete",
                kwargs={"pk": task.pk},
            )
        )

        assert response.status_code == 302

    def test_delete_status_code(self, client, user, task):
        client.force_login(user)

        response = client.get(
            reverse(
                "task:delete",
                kwargs={"pk": task.pk},
            )
        )

        assert response.status_code == 200

    def test_delete_template(self, client, user, task):
        client.force_login(user)

        response = client.get(
            reverse(
                "task:delete",
                kwargs={"pk": task.pk},
            )
        )

        assert "task/delete.html" in [
            template.name
            for template in response.templates
        ]

    def test_delete_task(self, client, user, task):
        client.force_login(user)

        task_id = task.pk

        response = client.post(
            reverse(
                "task:delete",
                kwargs={"pk": task.pk},
            )
        )

        assert response.status_code == 302
        assert not Task.objects.filter(pk=task_id).exists()

    def test_user_cannot_delete_another_users_task(
        self,
        client,
        user,
        another_task,
    ):
        client.force_login(user)

        response = client.post(
            reverse(
                "task:delete",
                kwargs={"pk": another_task.pk},
            )
        )

        assert response.status_code == 404
        assert Task.objects.filter(pk=another_task.pk).exists()'''