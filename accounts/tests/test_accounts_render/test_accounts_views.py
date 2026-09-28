import pytest

from django.urls import reverse


from task.models import Task

# ============================================================
# Register
# ============================================================


@pytest.mark.django_db
class TestDashboardView:

    def test_unauthenticated(self, client):
        url = reverse("task:dashboard")

        response = client.get(url)

        assert response.status_code == 302
        assert response.url.startswith(reverse("accounts:login"))

    def test_authenticated(self, client, user):
        client.force_login(user)

        url = reverse("task:dashboard")

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_all_tasks(self, client, user, task, completed_task):
        client.force_login(user)

        assert response.resolver_match.func.view_class is RegisterView


# ============================================================
# Login
# ============================================================

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
        assert "form" in response.context

    def test_view_class(self, client):
        response = client.get(reverse("accounts:login"))

        assert response.resolver_match.func.view_class is CustomLoginView

    def test_uses_custom_authentication_form(self):
        assert (
            CustomLoginView.authentication_form.__name__
            == "CustomAuthenticationForm"
        )


# ============================================================
# Logout
# ============================================================


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

    def test_view_class(self, client):
        response = client.get(reverse("accounts:logout_confirm"))

        assert response.resolver_match.func.view_class is LogoutConfirmView


# ============================================================
# Password Reset
# ============================================================


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

    def test_view_class(self, client):
        response = client.get(reverse("accounts:password_reset"))

        assert (
            response.resolver_match.func.view_class is CustomPasswordResetView
        )


# ============================================================
# Password Reset Confirm
# ============================================================


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

    def test_view_class(self, client):
        url = reverse(
            "accounts:password_reset_confirm",
            kwargs={
                "uidb64": "invalid",
                "token": "invalid-token",
            },
        )

        response = client.get(url)

        assert (
            response.resolver_match.func.view_class
            is CustomPasswordResetConfirmView
        )


# ============================================================
# Password Change
# ============================================================


@pytest.mark.django_db
class TestTaskDetailView:

    def test_unauthenticated(self, client, task):
        url = reverse(
            "task:detail",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 302
        assert response.url.startswith(reverse("accounts:login"))

    def test_owner(self, client, user, task):
        client.force_login(user)

        url = reverse(
            "task:detail",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_view_class(self, client):
        response = client.get(reverse("accounts:password_change"))

        assert response.resolver_match.func.view_class is PasswordChangeView


# ============================================================
# Password Change Confirm
# ============================================================


@pytest.mark.django_db
class TestTaskCreateView:

    def test_unauthenticated(self, client):
        url = reverse("task:create")

        response = client.get(url)

        assert response.status_code == 302
        assert response.url.startswith(reverse("accounts:login"))

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

        created_task = Task.objects.get(title="New Task")

        assert created_task.user == user
        assert created_task.description == "New task description"
        assert created_task.done is False

    def test_view_class(self, client):
        response = client.get(reverse("accounts:password_change_done"))

        assert (
            response.resolver_match.func.view_class
            is PasswordChangeConfirmView
        )


# ============================================================
# Profile
# ============================================================


@pytest.mark.django_db
class TestTaskUpdateView:

    def test_unauthenticated(self, client, task):
        url = reverse(
            "task:update",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 302
        assert response.url.startswith(reverse("accounts:login"))

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

    def test_other_user_profile(
        self,
        client,
        verified_user,
        another_user,
    ):
        client.force_login(verified_user)

        url = reverse(
            "task:update",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 404

    def test_view_class(self, client, verified_user):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile",
            kwargs={"pk": verified_user.profile.pk},
        )

        response = client.get(url)

        assert response.resolver_match.func.view_class is ProfileView


# ============================================================
# Profile Update
# ============================================================


@pytest.mark.django_db
class TestTaskDeleteView:

    def test_unauthenticated(self, client, task):
        url = reverse(
            "task:delete",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 302
        assert response.url.startswith(reverse("accounts:login"))

    def test_owner(self, client, user, task):
        client.force_login(user)

        url = reverse(
            "task:delete",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["form"].instance == verified_user.profile

    def test_other_user_profile(
        self,
        client,
        verified_user,
        another_user,
    ):
        client.force_login(verified_user)

        url = reverse(
            "task:delete",
            kwargs={"pk": task.pk},
        )

        response = client.get(url)

        assert response.status_code == 404

    def test_view_class(self, client, verified_user):
        client.force_login(verified_user)

        url = reverse(
            "accounts:profile_edit",
            kwargs={"pk": verified_user.profile.pk},
        )

        response = client.get(url)

        assert response.resolver_match.func.view_class is ProfileUpdateView
