from django.urls import path
from .views import DashboardView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView

app_name = "task"
urlpatterns = [

    path(
        'dashboard/',
         DashboardView.as_view(),
         name='dashboard'),
    path(
        "detail/<int:pk>/"
         ,TaskDetailView.as_view(),
         name='detail'),
    path(
        "create/",
        TaskCreateView.as_view(),
        name='create'
    ),
    path(
        "update/<int:pk>/",
        TaskUpdateView.as_view(),
        name='update'
    ),
    path(
        "delete/<int:pk>/",
        TaskDeleteView.as_view(),
        name='delete'
    ),
]