from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from task.forms import TaskForm
from task.models import Task


# Create your views here.

class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "task/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        user_tasks = Task.objects.filter(
            user=self.request.user
        )

        # Search
        query = self.request.GET.get("q", "").strip()

        if query:
            user_tasks = user_tasks.filter(
                title__icontains=query
            )

        # Status
        status = self.request.GET.get("status", "all")

        if status == "pending":

            pending_list = user_tasks.filter(done=False)
            completed_list = Task.objects.none()

        elif status == "completed":

            pending_list = Task.objects.none()
            completed_list = user_tasks.filter(done=True)

        else:

            pending_list = user_tasks.filter(done=False)
            completed_list = user_tasks.filter(done=True)

        # Context
        context["status"] = status
        context["query"] = query

        context["pending_list"] = pending_list
        context["completed_list"] = completed_list

        # Statistics
        all_user_tasks = Task.objects.filter(
            user=self.request.user
        )

        context["total_tasks"] = all_user_tasks.count()

        context["pending_count"] = all_user_tasks.filter(
            done=False
        ).count()

        context["completed_count"] = all_user_tasks.filter(
            done=True
        ).count()

        return context

class TaskDetailView(LoginRequiredMixin,DetailView):
    template_name = 'task/detail.html'
    model = Task
    def get_queryset(self):
        return Task.objects.select_related('user').filter(user=self.request.user)



class TaskCreateView(LoginRequiredMixin,CreateView):
    template_name = 'task/create.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task:dashboard")
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'task/update.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task:dashboard")
    def get_queryset(self):
        return Task.objects.select_related('user').filter(user=self.request.user)


class TaskDeleteView(LoginRequiredMixin,DeleteView):
    template_name = 'task/delete.html'
    model = Task
    success_url = reverse_lazy("task:dashboard")
    def get_queryset(self):
        return Task.objects.select_related('user').filter(user=self.request.user)

