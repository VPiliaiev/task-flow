from django.urls import path

from tasks.views import (
    IndexView,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView, TaskDetailView, WorkerListView, WorkerCreateView, WorkerUpdateView, WorkerDeleteView,
    WorkerDetailView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),

    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
]

app_name = "tasks"
