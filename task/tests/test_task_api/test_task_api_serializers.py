'''import pytest

from task.api.v1.serializers import TaskModelSerializer


@pytest.mark.django_db
class TestTaskModelSerializer:

    def test_serializer_fields(
        self,
        task,
        list_request,
    ):
        serializer = TaskModelSerializer(
            task,
            context={"request": list_request},
        )

        assert set(serializer.data.keys()) == {
            "id",
            "title",
            "user",
            "desc",
            "done",
            "task_url",
        }

    def test_serializer_task_data(
        self,
        task,
        list_request,
    ):
        serializer = TaskModelSerializer(
            task,
            context={"request": list_request},
        )

        assert serializer.data["id"] == task.id
        assert serializer.data["title"] == task.title
        assert serializer.data["user"] == task.user.id
        assert serializer.data["desc"] == task.get_description()
        assert serializer.data["done"] is False
        assert "description" not in serializer.data

    def test_user_is_read_only(self, task):
        serializer = TaskModelSerializer(task)

        assert serializer.fields["user"].read_only is True

    def test_task_url_is_read_only(self, task):
        serializer = TaskModelSerializer(task)

        assert serializer.fields["task_url"].read_only is True

    def test_desc_is_read_only(self, task):
        serializer = TaskModelSerializer(task)

        assert serializer.fields["desc"].read_only is True

    def test_list_representation(
        self,
        task,
        list_request,
    ):
        serializer = TaskModelSerializer(
            task,
            context={"request": list_request},
        )

        assert "description" not in serializer.data
        assert "desc" in serializer.data
        assert "task_url" in serializer.data

        assert serializer.data["desc"] == task.get_description()

    def test_detail_representation(
        self,
        task,
        detail_request,
    ):
        serializer = TaskModelSerializer(
            task,
            context={"request": detail_request},
        )

        assert "description" in serializer.data
        assert "desc" not in serializer.data
        assert "task_url" not in serializer.data

        assert serializer.data["description"] == task.description

    def test_task_url(
        self,
        task,
        list_request,
    ):
        serializer = TaskModelSerializer(
            task,
            context={"request": list_request},
        )

        expected_url = list_request.build_absolute_uri(task.id)

        assert serializer.data["task_url"] == expected_url

    def test_create_task(
        self,
        user,
        list_request,
    ):
        list_request.user = user

        serializer = TaskModelSerializer(
            data={
                "title": "New Task",
                "description": "New task description",
                "done": False,
            },
            context={"request": list_request},
        )

        assert serializer.is_valid()

        task = serializer.save()

        assert task.title == "New Task"
        assert task.description == "New task description"
        assert task.done is False
        assert task.user == user

    def test_invalid_title(
        self,
        list_request,
    ):
        serializer = TaskModelSerializer(
            data={
                "title": "",
                "description": "Test description",
                "done": False,
            },
            context={"request": list_request},
        )

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_invalid_description(
        self,
        list_request,
    ):
        serializer = TaskModelSerializer(
            data={
                "title": "Test Task",
                "description": "",
                "done": False,
            },
            context={"request": list_request},
        )

        assert not serializer.is_valid()
        assert "description" in serializer.errors

    def test_user_cannot_be_provided_in_input(
        self,
        user,
        another_user,
        list_request,
    ):
        list_request.user = user

        serializer = TaskModelSerializer(
            data={
                "title": "New Task",
                "description": "Test description",
                "done": False,
                "user": another_user.id,
            },
            context={"request": list_request},
        )

        assert serializer.is_valid()

        task = serializer.save()

        assert task.user == user
        assert task.user != another_user
'''