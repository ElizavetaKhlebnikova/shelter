from datetime import timedelta
from http import HTTPStatus
import uuid

from django.test import Client, TestCase
from django.urls import reverse
from django.utils.timezone import now
from django.conf import settings
from django.test.utils import override_settings

from unittest.mock import patch

from users.forms import UserLoginForm, UserProfileForm
from users.models import EmailVerification, User
from .services.verification import send_verification_email, create_and_send_email_verification_object
from .tasks import send_email_verification


class TestEmailServices(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', email='test@example.com')
        self.expiration = now() + timedelta(hours=48)
        self.record = EmailVerification.objects.create(user=self.user, code=uuid.uuid4(), expiration=self.expiration)

    @patch('users.services.verification.send_mail')
    def test_send_verification_email(self, mock_send_mail):
        # проверка однократного вызова функции send_mail
        send_verification_email(self.record)

        # ожидаемое содержание письма:
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.record.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        expected_subject = f'Подтверждение учётной записи для {self.user}'
        expected_message_start = 'Для подтверждения учетной записи для {} перейдите по ссылке {}, {}'.format(
            self.user.username,
            verification_link,
            self.expiration
        )

        # Проверка факта отправки письма
        self.assertTrue(mock_send_mail.called)
        mock_send_mail.assert_called_once()
        # Получаем аргументы, с которыми была вызвана mock-функция
        sent_args = mock_send_mail.call_args
        # Проверяем тему письма
        self.assertEqual(sent_args[1]['subject'], expected_subject)
        # Проверяем, совпадает ли текст сообщения с ожидаемым содержимым письма
        self.assertTrue(sent_args[1]['message'].startswith(expected_message_start))
        print(len(EmailVerification.objects.all()))

    @patch('users.services.verification.send_verification_email')
    def test_create_and_send_email_verification_object(self, mock_send_verification_email):
        create_and_send_email_verification_object(self.user.id)
        # так как в setUp уже был создан один объект EmailVerification, то сейчас мы ожидаем добавление второго
        self.assertEqual(EmailVerification.objects.count(), 2)
        # проверяем запуск функции отправки письма
        mock_send_verification_email.assert_called_once()
        # проверяем корректность данных объекта EmailVerification
        email_verification = EmailVerification.objects.filter(user__username=self.user.username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification[1].expiration.date(),
            (now() + timedelta(hours=48)).date()
        )


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

    @patch('users.tasks.send_email_verification.delay')
    def test_user_registration_post_success(self, mock_send_email):
        response = self.client.post(self.path, self.data)
        username = self.data['username']

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'), fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(username=username).exists())
        self.assertEqual(User.objects.count(), 1)

    def test_user_registration_post_name_error(self):
        username = self.data['username']
        User.objects.create(username=username)
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)

    def test_user_registration_post_email_error(self):
        email = self.data['email']
        User.objects.create(email=email)
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким Email уже существует.', html=True)


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
        # UserProfileViewTestCase.test_profile_view
