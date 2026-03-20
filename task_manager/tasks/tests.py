from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from .models import Task

class TaskCRUDTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.status = Status.objects.create(name='новый')
        self.task = Task.objects.create(
            name='Тестовая задача',
            author=self.user1,
            status=self.status
        )

    # def test_task_list_unauthenticated(self):
    #     response = self.client.get(reverse('tasks:tasks_list'))
    #     self.assertRedirects(response, f"{reverse('login')}?next={reverse('tasks:tasks_list')}")

    def test_task_list_authenticated(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('tasks:tasks_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая задача')

    def test_task_create(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('tasks:task_create'), {
            'name': 'Новая задача',
            'status': self.status.pk,
            'executor': self.user2.pk
        })
        self.assertRedirects(response, reverse('tasks:tasks_list'))
        self.assertTrue(Task.objects.filter(name='Новая задача').exists())
        task = Task.objects.get(name='Новая задача')
        self.assertEqual(task.author, self.user1)

    def test_task_update(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('tasks:task_update', args=[self.task.pk]), {
            'name': 'Обновлённая задача',
            'status': self.status.pk
        })
        self.assertRedirects(response, reverse('tasks:tasks_list'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Обновлённая задача')

    def test_task_delete_by_author(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('tasks:task_delete', args=[self.task.pk]))
        self.assertRedirects(response, reverse('tasks:tasks_list'))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_by_non_author(self):
        self.client.login(username='user2', password='pass')
        response = self.client.post(reverse('tasks:task_delete', args=[self.task.pk]))
        self.assertRedirects(response, reverse('tasks:tasks_list'))
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_detail(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('tasks:task_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая задача')

    def test_task_unique_name(self):
        self.client.login(username='user1', password='pass')
        self.client.post(reverse('tasks:task_create'), {
            'name': 'Уникальная задача',
            'status': self.status.pk,
        })
        response = self.client.post(reverse('tasks:task_create'), {
            'name': 'Уникальная задача',
            'status': self.status.pk,
        })
        self.assertContains(response, "уже существует")
        self.assertEqual(Task.objects.filter(name='Уникальная задача').count(), 1)
