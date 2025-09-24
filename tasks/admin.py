from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import Position, Worker, TaskType, Task


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("first_name", "last_name", "position",)}),)
    list_filter = ("position",)
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "task_type", "priority", "deadline", "is_completed")
    list_filter = ("task_type", "priority", "is_completed")
    search_fields = ("name", "description")
    filter_horizontal = ("assignees",)
