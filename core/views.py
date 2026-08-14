from django.shortcuts import render
from django.views.generic import TemplateView
from task.models import Task
# Create your views here.
from django.views.generic import TemplateView
from task.models import Task


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:

            tasks = Task.objects.filter(
                user=self.request.user
            )

            context["total_tasks"] = tasks.count()

            context["pending_count"] = tasks.filter(
                done=False
            ).count()

            context["completed_count"] = tasks.filter(
                done=True
            ).count()

            context["recent_tasks"] = tasks.order_by(
                "-created_at"
            )[:3]

        return context