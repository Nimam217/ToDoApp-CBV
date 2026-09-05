from task.forms import TaskForm


class TestTaskForm:

    def test_form_fields(self):
        form = TaskForm()

        assert list(form.fields.keys()) == [
            "title",
            "description",
            "done",
        ]

    def test_form_valid_data(self):
        form = TaskForm(
            data={
                "title": "Test task",
                "description": "Test description",
                "done": False,
            }
        )

        assert form.is_valid()

    def test_title_required(self):
        form = TaskForm(
            data={
                "title": "",
                "description": "Test description",
                "done": False,
            }
        )

        assert not form.is_valid()
        assert "title" in form.errors

    def test_description_required(self):
        form = TaskForm(
            data={
                "title": "Test task",
                "description": "",
                "done": False,
            }
        )

        assert not form.is_valid()
        assert "description" in form.errors

    def test_done_not_required(self):
        form = TaskForm(
            data={
                "title": "Test task",
                "description": "Test description",
            }
        )

        assert form.is_valid()

    def test_title_widget(self):
        form = TaskForm()

        widget = form.fields["title"].widget

        assert widget.__class__.__name__ == "TextInput"
        assert widget.attrs["class"] == "form-control"
        assert widget.attrs["placeholder"] == "Enter task title"

    def test_description_widget(self):
        form = TaskForm()

        widget = form.fields["description"].widget

        assert widget.__class__.__name__ == "Textarea"
        assert widget.attrs["class"] == "form-control"
        assert widget.attrs["placeholder"] == "Describe your task..."
        assert widget.attrs["rows"] == 5

    def test_done_widget(self):
        form = TaskForm()

        widget = form.fields["done"].widget

        assert widget.__class__.__name__ == "CheckboxInput"
        assert widget.attrs["class"] == "form-check-input"
