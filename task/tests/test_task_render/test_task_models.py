'''import pytest

from django.core.exceptions import ValidationError

from task.models import Task


@pytest.mark.django_db
class TestTaskModel:

    def test_create_task(self, task, user):
        assert task.title == "Test Task"
        assert task.description == "Test task description"
        assert task.user == user
        assert task.done is False

    def test_task_str(self, task):
        assert str(task) == "Test Task"

    def test_task_get_description(self, task):
        assert task.get_description() == "Test "

    def test_task_done_default(self, user):
        task = Task.objects.create(
            title="New Task",
            description="New task description",
            user=user,
        )

        assert task.done is False

    def test_task_created_at(self, task):
        assert task.created_at is not None

    def test_task_updated_at(self, task):
        assert task.updated_at is not None

    def test_task_belongs_to_user(self, task, user):
        assert task.user == user

    def test_user_can_have_multiple_tasks(self, user):
        task_1 = Task.objects.create(
            title="Task 1",
            description="Description 1",
            user=user,
        )

        task_2 = Task.objects.create(
            title="Task 2",
            description="Description 2",
            user=user,
        )

        assert task_1.user == user
        assert task_2.user == user
        assert user.task_set.count() == 2

    def test_task_deleted_when_user_deleted(self, task, user):
        task_id = task.id

        user.delete()

        assert not Task.objects.filter(id=task_id).exists()

    def test_task_title_max_length(self):
        task = Task(
            title="a" * 101,
            description="Test description",
        )

        with pytest.raises(ValidationError):
            task.full_clean()

    def test_task_description_required(self, user):
        task = Task(
            title="Test Task",
            description="",
            user=user,
        )

        with pytest.raises(ValidationError):
            task.full_clean()'''