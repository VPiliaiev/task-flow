from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import TaskForm, WorkerCreationForm, TaskNameSearchForm, WorkerUsernameSearchForm
from tasks.models import Task, Worker


class IndexView(generic.TemplateView):
    template_name = "tasks/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_workers"] = Worker.objects.count()
        context["num_tasks"] = Task.objects.count()
        context["num_completed_tasks"] = Task.objects.filter(is_completed=True).count()

        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskNameSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskNameSearchForm(initial={"name": name})
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    context_object_name = "worker_list"
    template_name = "tasks/worker_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        form = WorkerUsernameSearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data["username"]:
            queryset = queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = WorkerUsernameSearchForm(self.request.GET)
        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    template_name = "tasks/worker_detail.html"
    queryset = get_user_model().objects.select_related("position")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = self.object.assigned_tasks.all()
        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreationForm
    template_name = "tasks/worker_form.html"
    success_url = reverse_lazy("tasks:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerCreationForm
    template_name = "tasks/worker_form.html"
    success_url = reverse_lazy("tasks:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    template_name = "tasks/worker_confirm_delete.html"
    success_url = reverse_lazy("tasks:worker-list")
