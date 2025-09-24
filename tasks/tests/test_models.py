from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Position, TaskType, Task
from datetime import datetime, timedelta


class ModelTests(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="Developer")
        self.assertEqual(str(position), "Developer")

    def test_worker_str_with_position(self):
        position = Position.objects.create(name="Manager")
        worker = get_user_model().objects.create_user(
            username="worker1",
            password="test123",
            position=position
        )
        self.assertEqual(str(worker), f"worker1 ({position})")

    def test_worker_str_without_position(self):
        worker = get_user_model().objects.create_user(
            username="worker2",
            password="test123"
        )
        self.assertEqual(str(worker), "worker2")

    def test_worker_get_absolute_url(self):
        worker = get_user_model().objects.create_user(
            username="worker3",
            password="test123"
        )
        self.assertEqual(
            worker.get_absolute_url(),
            reverse("tasks:worker-detail", kwargs={"pk": worker.pk})
        )

    def test_tasktype_str(self):
        task_type = TaskType.objects.create(name="Bug")
        self.assertEqual(str(task_type), "Bug")

    def test_task_str(self):
        task_type = TaskType.objects.create(name="Feature")
        worker = get_user_model().objects.create_user(
            username="worker4",
            password="test123"
        )
        task = Task.objects.create(
            name="Implement login",
            description="Add login functionality",
            deadline=datetime.now() + timedelta(days=7),
            priority=Task.PriorityChoices.HIGH,
            task_type=task_type,
        )
        task.assignees.add(worker)
        self.assertEqual(str(task), f"{task.name} [{task.priority}]")
