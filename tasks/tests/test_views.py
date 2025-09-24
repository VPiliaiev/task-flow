from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Position, Task, TaskType
from datetime import datetime, timedelta


class PublicWorkerTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="worker1",
            password="pass123",
            position=self.position
        )

    def test_login_required_list(self):
        response = self.client.get(reverse("tasks:worker-list"))
        self.assertRedirects(response, f"/accounts/login/?next=/workers/")

    def test_login_required_detail(self):
        response = self.client.get(reverse("tasks:worker-detail", args=[self.worker.pk]))
        self.assertRedirects(response, f"/accounts/login/?next=/workers/{self.worker.pk}/")

    def test_login_required_create(self):
        response = self.client.get(reverse("tasks:worker-create"))
        self.assertRedirects(response, "/accounts/login/?next=/workers/create/")

    def test_login_required_delete(self):
        response = self.client.get(reverse("tasks:worker-delete", args=[self.worker.pk]))
        self.assertRedirects(response, f"/accounts/login/?next=/workers/{self.worker.pk}/delete/")


class PrivateWorkerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username="admin", password="pass123")
        self.client.force_login(self.user)
        self.position = Position.objects.create(name="Developer")

        self.workers = []
        for i in range(7):
            worker = get_user_model().objects.create_user(
                username=f"worker{i}",
                password="pass123",
                position=self.position
            )
            self.workers.append(worker)
        self.worker = self.workers[0]

    def test_worker_list_view(self):
        response = self.client.get(reverse("tasks:worker-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_list.html")

    def test_worker_detail_view(self):
        response = self.client.get(reverse("tasks:worker-detail", args=[self.worker.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.worker.username)

    def test_worker_create_view(self):
        data = {
            "username": "worker_new",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "John",
            "last_name": "Doe",
            "position": self.position.pk
        }
        response = self.client.post(reverse("tasks:worker-create"), data)
        self.assertRedirects(response, reverse("tasks:worker-list"))
        self.assertTrue(get_user_model().objects.filter(username="worker_new").exists())

    def test_worker_update_view(self):
        data = {
            "username": "worker_updated",
            "first_name": "Jane",
            "last_name": "Doe",
            "position": self.position.pk
        }
        response = self.client.post(reverse("tasks:worker-update", args=[self.worker.pk]), data)
        self.assertRedirects(response, reverse("tasks:worker-list"))
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.username, "worker_updated")
        self.assertEqual(self.worker.first_name, "Jane")

    def test_worker_delete_view(self):
        response = self.client.post(reverse("tasks:worker-delete", args=[self.worker.pk]))
        self.assertRedirects(response, reverse("tasks:worker-list"))
        self.assertFalse(get_user_model().objects.filter(pk=self.worker.pk).exists())

    def test_pagination(self):
        response = self.client.get(reverse("tasks:worker-list"))
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["worker_list"]), 5)

    def test_search(self):
        response = self.client.get(reverse("tasks:worker-list"), {"username": "worker1"})
        self.assertContains(response, "worker1")
        self.assertNotContains(response, "worker2")


class PublicTaskTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(username="worker1", password="pass123",
                                                           position=self.position)
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Test Task",
            description="Description",
            deadline=datetime.now() + timedelta(days=1),
            priority="High",
            task_type=self.task_type,
            is_completed=False
        )
        self.task.assignees.add(self.worker)

    def test_login_required_list(self):
        response = self.client.get(reverse("tasks:task-list"))
        self.assertRedirects(response, "/accounts/login/?next=/tasks/")

    def test_login_required_detail(self):
        response = self.client.get(reverse("tasks:task-detail", args=[self.task.pk]))
        self.assertRedirects(response, f"/accounts/login/?next=/tasks/{self.task.pk}/")

    def test_login_required_create(self):
        response = self.client.get(reverse("tasks:task-create"))
        self.assertRedirects(response, "/accounts/login/?next=/tasks/create/")

    def test_login_required_delete(self):
        response = self.client.get(reverse("tasks:task-delete", args=[self.task.pk]))
        self.assertRedirects(response, f"/accounts/login/?next=/tasks/{self.task.pk}/delete/")


class PrivateTaskTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username="admin", password="pass123")
        self.client.force_login(self.user)

        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(username="worker1", password="pass123",
                                                           position=self.position)
        self.task_type = TaskType.objects.create(name="Bug")

        self.tasks = []
        for i in range(7):
            task = Task.objects.create(
                name=f"Task {i}",
                description="Desc",
                deadline=datetime.now() + timedelta(days=i),
                priority="Medium",
                task_type=self.task_type,
                is_completed=(i % 2 == 0)
            )
            task.assignees.add(self.worker)
            self.tasks.append(task)
        self.task = self.tasks[0]

    def test_task_list_view(self):
        response = self.client.get(reverse("tasks:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_list.html")
        self.assertContains(response, self.task.name)

    def test_task_detail_view(self):
        response = self.client.get(reverse("tasks:task-detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_create_view(self):
        data = {
            "name": "New Task",
            "description": "Desc",
            "deadline": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M"),
            "priority": "Medium",
            "task_type": self.task_type.pk,
            "assignees": [self.worker.pk],
            "is_completed": False
        }
        response = self.client.post(reverse("tasks:task-create"), data)
        self.assertRedirects(response, reverse("tasks:task-list"))
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_task_update_view(self):
        data = {
            "name": "Updated Task",
            "description": "Desc Updated",
            "deadline": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M"),
            "priority": "Low",
            "task_type": self.task_type.pk,
            "assignees": [self.worker.pk],
            "is_completed": True
        }
        response = self.client.post(reverse("tasks:task-update", args=[self.task.pk]), data)
        self.assertRedirects(response, reverse("tasks:task-list"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")
        self.assertTrue(self.task.is_completed)

    def test_task_delete_view(self):
        response = self.client.post(reverse("tasks:task-delete", args=[self.task.pk]))
        self.assertRedirects(response, reverse("tasks:task-list"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_pagination(self):
        response = self.client.get(reverse("tasks:task-list"))
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["task_list"]), 5)

    def test_search(self):
        response = self.client.get(reverse("tasks:task-list"), {"name": "Task 1"})
        self.assertContains(response, "Task 1")
        self.assertNotContains(response, "Task 2")
