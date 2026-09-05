from django import forms
from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = (
            "title",
            "description",
            "done",
        )

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter task title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe your task...",
                    "rows": 5,
                }
            ),
            "done": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }
