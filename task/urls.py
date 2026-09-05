from django.urls import path, include
from .views import (
    DashboardView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
)

app_name = "task"
urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("detail/<int:pk>/", TaskDetailView.as_view(), name="detail"),
    path("create/", TaskCreateView.as_view(), name="create"),
    path("update/<int:pk>/", TaskUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", TaskDeleteView.as_view(), name="delete"),
    path(
        "api/v1/",
        include(
            ("task.api.v1.urls", "task_api_v1"),
            namespace="task_api_v1",
        ),
    ),
]
