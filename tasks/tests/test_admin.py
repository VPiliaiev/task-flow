from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Position, TaskType, Task


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)

        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="testworker",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Bugfix")
        self.task = Task.objects.create(
            name="Fix login bug",
            description="Error when logging in",
            task_type=self.task_type,
            priority="High",
            deadline="2025-12-31",
            is_completed=False,
        )
        self.task.assignees.add(self.worker)

    def test_position_listed_in_admin(self):
        url = reverse("admin:tasks_position_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.position.name)

    def test_position_detail_page(self):
        url = reverse("admin:tasks_position_change", args=[self.position.id])
        res = self.client.get(url)
        self.assertContains(res, self.position.name)

    def test_worker_listed_in_admin(self):
        url = reverse("admin:tasks_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.username)
        self.assertContains(res, self.worker.position.name)

    def test_worker_detail_page(self):
        url = reverse("admin:tasks_worker_change", args=[self.worker.id])
        res = self.client.get(url)
        self.assertContains(res, self.worker.position.name)

    def test_tasktype_listed_in_admin(self):
        url = reverse("admin:tasks_tasktype_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.task_type.name)

    def test_tasktype_detail_page(self):
        url = reverse("admin:tasks_tasktype_change", args=[self.task_type.id])
        res = self.client.get(url)
        self.assertContains(res, self.task_type.name)

    def test_task_listed_in_admin(self):
        url = reverse("admin:tasks_task_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.task.name)
        self.assertContains(res, self.task.task_type.name)

    def test_task_detail_page(self):
        url = reverse("admin:tasks_task_change", args=[self.task.id])
        res = self.client.get(url)
        self.assertContains(res, self.task.name)
        self.assertContains(res, self.task.task_type.name)
