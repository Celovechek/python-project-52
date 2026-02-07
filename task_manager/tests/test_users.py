from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserCRUDTest(TestCase):
    fixtures = ['users.json']

    def test_user_list_accessible(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user1')
        self.assertContains(response, 'user2')

    def test_user_create(self):
        data = {
            'username': 'jhondoe',
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(reverse('user_create'), data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='jhondoe').exists())

    def test_user_update_self(self):
        user1 = User.objects.get(username='user1')
        self.client.login(username='user1', password='password123')
        response = self.client.post(
            reverse('user_update', args=[user1.pk]),
            {
                'username': user1.username,
                'first_name': 'Kotik',
                'last_name': 'Pushistiy'
            }
        )
        self.assertRedirects(response, reverse('users_list'))
        user1.refresh_from_db()
        self.assertEqual(user1.first_name, 'Kotik')

    def test_user_update_other_forbidden(self):
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        self.client.login(username='user1', password='password123')
        old_name = user2.first_name
        response = self.client.post(
            reverse('user_update', args=[user2.pk]),
            {
                'username': user2.username,
                'first_name': 'Хакер',
                'last_name': 'X'
            }
        )
        self.assertRedirects(response, reverse('users_list'))
        user2.refresh_from_db()
        self.assertEqual(user2.first_name, old_name)

    def test_user_delete_self(self):
        user1 = User.objects.get(username='user1')
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('user_delete', args=[user1.pk]))
        self.assertRedirects(response, reverse('users_list'))
        self.assertFalse(User.objects.filter(pk=user1.pk).exists())

    def test_user_delete_other_forbidden(self):
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('user_delete', args=[user2.pk]))
        self.assertRedirects(response, reverse('users_list'))
        self.assertTrue(User.objects.filter(pk=user2.pk).exists())

    def test_login_redirect(self):
        response = self.client.post(reverse('login'), {
            'username': 'user1',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('home'))

    def test_logout(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
