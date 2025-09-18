from django.urls import path

from tasks.views import (
    IndexView,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView, TaskDetailView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),

]

app_name = "tasks"
