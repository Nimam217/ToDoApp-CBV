from django.contrib import admin
from .models import Task


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "done", "created_at", "updated_at", "user")
    list_filter = ("done", "created_at", "updated_at", "user")
    search_fields = ("title", "user")


admin.site.register(Task, TaskAdmin)
