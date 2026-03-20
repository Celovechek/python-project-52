from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.views import View
from task_manager.tasks.models import Task

def index(request):
    return render(request, 'index.html')

class UserListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно зарегистрирован")
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users_list')

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения другого пользователя.")
        return redirect('users_list')

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно изменён")
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users_list')

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(
            self.request,
            "У вас нет прав для удаления другого пользователя."
        )
        return redirect('users_list')

    def form_valid(self, form):
        user = self.get_object()

        # Проверяем, связан ли пользователь с задачами
        if Task.objects.filter(author=user).exists() or Task.objects.filter(executor=user).exists():
            messages.error(
                self.request,
                "Невозможно удалить пользователя, потому что он используется"
            )
            return redirect(self.success_url)

        messages.success(self.request, "Пользователь успешно удалён")
        return super().form_valid(form)

class UserLoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)

class UserLogoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "Вы разлогинены")
        return redirect('home')
