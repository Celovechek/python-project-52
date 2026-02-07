from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from .models import Status
from .forms import StatusForm
from urllib.parse import urlencode


class StatusBaseView(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        login_url = reverse('login')
        next_url = self.request.get_full_path()
        return redirect(f"{login_url}?{urlencode({'next': next_url})}")


class StatusListView(StatusBaseView, ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusCreateView(StatusBaseView, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/statuses_create.html'
    success_url = reverse_lazy('statuses:statuses_list')

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно создан")
        return super().form_valid(form)


class StatusUpdateView(StatusBaseView, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/statuses_update.html'
    success_url = reverse_lazy('statuses:statuses_list')

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно изменён")
        return super().form_valid(form)


class StatusDeleteView(StatusBaseView, DeleteView):
    model = Status
    template_name = 'statuses/statuses_delete.html'
    success_url = reverse_lazy('statuses:statuses_list')

    def form_valid(self, form):
        # Временно закомментировано — раскомментируете на шаге "Задачи"
        # from task_manager.tasks.models import Task
        # if Task.objects.filter(status=self.object).exists():
        #     messages.error(
        #         self.request,
        #         "Невозможно удалить статус, потому что он используется"
        #     )
        #     return self.form_invalid(form)
        messages.success(self.request, "Статус успешно удалён")
        return super().form_valid(form)
