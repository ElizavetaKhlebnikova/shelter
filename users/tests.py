from datetime import timedelta
from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.forms import UserLoginForm, UserProfileForm
from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:registration')
        self.data = {
            'first_name': 'Liza',
            'last_name': 'Khlebnikova',
            'username': 'liza',
            'email': 'liza-khlebnikova@yandex.ru',
            'password1': '1234lizabelka',
            'password2': '1234lizabelka',
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'HappyVeganShelter - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')
        # UserRegistrationViewTestCase.test_user_registration_get

    def test_user_registration_post_success(self):
        response = self.client.post(self.path, self.data)
        username = self.data['username']

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'), fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(username=username).exists())

        # check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification[0].expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_name_error(self):
        username = self.data['username']
        User.objects.create(username=username)
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
        # UserRegistrationViewTestCase.test_user_registration_post_error

    def test_user_registration_post_email_error(self):
        email = self.data['email']
        User.objects.create(email=email)
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким Email уже существует.', html=True)
        # UserRegistrationViewTestCase.test_user_registration_post_email_error


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.login_url = reverse('users:login')

    def test_login_page_loads_successfully(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], UserLoginForm)
        # UserLoginViewTestCase.test_login_page_loads_successfully

    def test_login_successful(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, reverse('index'))

    def test_login_failure(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
    # UserLoginViewTestCase.test_login_page_download_successfully


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        # создаем тестового пользователя и клиент тестирования Django
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()

    def test_profile_view(self):
        # войти в систему
        self.client.login(username='testuser', password='testpass')
        # получить расположение страницы профиля
        response = self.client.get(reverse('users:profile'))
        # проверить, что страница была успешно получена (статус код 200)
        self.assertEqual(response.status_code, 200)
        # проверить, что текущий пользователь является пользователем, возвращаемым методом `get_object`
        self.assertEqual(response.context['object'], self.user)
        # проверить, что форма UserProfileForm используется в представлении
        self.assertIsInstance(response.context['form'], UserProfileForm)
        # проверить, что в ответе используется правильный шаблон
        self.assertTemplateUsed(response, 'users/profile.html')
