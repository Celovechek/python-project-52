from django.db import models
from django.contrib.auth.models import User
from task_manager.statuses.models import Status

class Task(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Имя", error_messages={'unique': 'Задача с этим именем уже существует'})
    description = models.TextField(blank=True, verbose_name="Описание")
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name="Статус"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name="Автор"
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name="Исполнитель"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
