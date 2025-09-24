from django.test import TestCase
from django.contrib.auth import get_user_model
from tasks.models import TaskType, Position
from tasks.forms import (
    TaskForm,
    TaskNameSearchForm,
    TaskStatusFilterForm,
    WorkerCreationForm,
    WorkerUsernameSearchForm,
)


class TaskFormTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug")
        self.worker1 = get_user_model().objects.create_user(
            username="worker1", password="pass123"
        )
        self.worker2 = get_user_model().objects.create_user(
            username="worker2", password="pass123"
        )

    def test_valid_task_form(self):
        data = {
            "name": "Fix bug",
            "description": "Critical bug",
            "deadline": "2025-12-31T12:00",
            "priority": "High",
            "task_type": self.task_type.pk,
            "assignees": [self.worker1.pk, self.worker2.pk],
            "is_completed": False,
        }
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertEqual(task.name, "Fix bug")
        self.assertEqual(list(task.assignees.all()), [self.worker1, self.worker2])

    def test_invalid_task_form_missing_name(self):
        data = {
            "description": "Critical bug",
            "deadline": "2025-12-31T12:00",
            "priority": "High",
            "task_type": self.task_type.pk,
            "assignees": [self.worker1.pk],
            "is_completed": False,
        }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TaskNameSearchFormTests(TestCase):
    def test_valid_search(self):
        form = TaskNameSearchForm(data={"name": "Fix bug"})
        self.assertTrue(form.is_valid())

    def test_empty_search(self):
        form = TaskNameSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())


class TaskStatusFilterFormTests(TestCase):
    def test_all_status(self):
        form = TaskStatusFilterForm(data={"status": ""})
        self.assertTrue(form.is_valid())

    def test_completed_status(self):
        form = TaskStatusFilterForm(data={"status": "completed"})
        self.assertTrue(form.is_valid())

    def test_invalid_status(self):
        form = TaskStatusFilterForm(data={"status": "invalid"})
        self.assertFalse(form.is_valid())


class WorkerCreationFormTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")

    def test_valid_worker_creation_form(self):
        data = {
            "username": "new_worker",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "John",
            "last_name": "Doe",
            "position": self.position.pk,
        }
        form = WorkerCreationForm(data=data)
        self.assertTrue(form.is_valid())
        worker = form.save()
        self.assertEqual(worker.username, "new_worker")
        self.assertEqual(worker.position, self.position)

    def test_invalid_worker_creation_form(self):
        data = {
            "username": "new_worker",
            "password1": "testpass123",
            "password2": "wrongpass",
            "first_name": "John",
            "last_name": "Doe",
            "position": self.position.pk,
        }
        form = WorkerCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class WorkerUsernameSearchFormTests(TestCase):
    def test_valid_username_search(self):
        form = WorkerUsernameSearchForm(data={"username": "worker1"})
        self.assertTrue(form.is_valid())

    def test_empty_username_search(self):
        form = WorkerUsernameSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())
