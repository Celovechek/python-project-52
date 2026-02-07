from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Status


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.status = Status.objects.create(name='новый')

    def test_status_list_unauthenticated(self):
        response = self.client.get(reverse('statuses:statuses_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('statuses:statuses_list')}")

    def test_status_list_authenticated(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('statuses:statuses_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'новый')

    def test_status_create(self):
        self.client.login(username='user', password='pass')
        response = self.client.post(reverse('statuses:status_create'), {'name': 'в работе'})
        self.assertRedirects(response, reverse('statuses:statuses_list'))
        self.assertTrue(Status.objects.filter(name='в работе').exists())

    def test_status_update(self):
        self.client.login(username='user', password='pass')
        response = self.client.post(
            reverse('statuses:status_update', args=[self.status.pk]),
            {'name': 'завершён'}
        )
        self.assertRedirects(response, reverse('statuses:statuses_list'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'завершён')

    def test_status_delete(self):
        self.client.login(username='user', password='pass')
        response = self.client.post(reverse('statuses:status_delete', args=[self.status.pk]))
        self.assertRedirects(response, reverse('statuses:statuses_list'))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
