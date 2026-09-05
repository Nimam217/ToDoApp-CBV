from django import forms
from django_filters import rest_framework as filters

from task.models import Task


class CustomFilterBackend(filters.FilterSet):

    from_this_date = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    to_this_date = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    is_done = filters.BooleanFilter(field_name="done")

    class Meta:
        model = Task
        fields = [
            "from_this_date",
            "to_this_date",
            "is_done",
        ]
