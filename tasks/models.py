from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        ordering = ["name"]
        verbose_name = "Position"
        verbose_name_plural = "Positions"

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers",
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["username"]
        verbose_name = "Worker"
        verbose_name_plural = "Workers"

    def __str__(self):
        return f"{self.username} ({self.position})" if self.position else self.username

    def get_absolute_url(self):
        return reverse("tasks:worker-detail", kwargs={"pk": self.pk})


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]
        verbose_name = "Task Type"
        verbose_name_plural = "Task Types"

    def __str__(self):
        return self.name


class Task(models.Model):
    class PriorityChoices(models.TextChoices):
        URGENT = "Urgent", "Urgent"
        HIGH = "High", "High"
        MEDIUM = "Medium", "Medium"
        LOW = "Low", "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
    )

    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        Worker,
        related_name="assigned_tasks"
    )

    class Meta:
        ordering = ["deadline", "priority"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f"{self.name} [{self.priority}]"
