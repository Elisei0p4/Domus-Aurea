from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from store.factories import UserFactory

class UsersViewsTests(TestCase):

    def setUp(self):
        self.user_password = 'a-very-strong-password'
        self.user_data_obj = UserFactory.build(password=self.user_password)
        self.user_data_dict = {
            'username': self.user_data_obj.username,
            'email': self.user_data_obj.email,
            'first_name': self.user_data_obj.first_name,
            'last_name': self.user_data_obj.last_name,
            'password1': self.user_password,
            'password2': self.user_password,
        }

        self.login_url = reverse('users:login')
        self.register_url = reverse('users:register')
        self.logout_url = reverse('users:logout')

    def test_login_page_loads(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_register_page_loads(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_successful_registration(self):
        """Тестирует успешную регистрацию и автоматический вход."""
        response = self.client.post(self.register_url, self.user_data_dict, follow=True)
        self.assertTrue(User.objects.filter(username=self.user_data_dict['username']).exists())
        self.assertRedirects(response, reverse('store:home'))
        self.assertContains(response, f'Аккаунт {self.user_data_dict["username"]} успешно создан!')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_registration_with_existing_username(self):
        """Тестирует регистрацию с уже существующим именем."""
        UserFactory(username=self.user_data_dict['username'])
        response = self.client.post(self.register_url, self.user_data_dict)

        self.assertContains(response, 'Пользователь с таким именем уже существует.')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_successful_login(self):
        """Тестирует успешный вход в систему."""
        UserFactory(username=self.user_data_dict['username'], password=self.user_password)

        login_data = {
            'username': self.user_data_dict['username'],
            'password': self.user_password
        }
        response = self.client.post(self.login_url, login_data, follow=True)

        self.assertRedirects(response, reverse('store:account'))
        self.assertContains(response, f'Добро пожаловать, {self.user_data_dict["username"]}!')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_failed_login(self):
        """Тестирует неудачную попытку входа."""
        response = self.client.post(self.login_url, {'username': 'wronguser', 'password': 'wrongpassword'}, follow=True)
        self.assertContains(response, 'Неверное имя пользователя или пароль.')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_successful_logout(self):
        """Тестирует выход из системы."""
        self.client.post(self.register_url, self.user_data_dict)

        response = self.client.post(self.logout_url, follow=True)
        self.assertRedirects(response, reverse('store:home'))
        self.assertContains(response, 'Вы успешно вышли из аккаунта.')
        self.assertFalse(response.context['user'].is_authenticated)