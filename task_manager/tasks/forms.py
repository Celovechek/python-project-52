from django import forms
from .models import Task
from django.contrib.auth.models import User
from task_manager.statuses.models import Status

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
