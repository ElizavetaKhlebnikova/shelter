import uuid
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


def send_verification_email(record):
    '''Создаёт текст письма пользователю и отправляет его'''
    link = reverse('users:email_verification', kwargs={'email': record.user.email, 'code': record.code})
    verification_link = f'{settings.DOMAIN_NAME}{link}'
    subject = f'Подтверждение учётной записи для {record.user.username}'
    message = 'Для подтверждения учетной записи для {} перейдите по ссылке {}, {}'.format(
        record.user.username,
        verification_link,
        record.expiration
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[record.user.email],
        fail_silently=False,
    )


def create_and_send_email_verification_object(user_id):
    '''Создаёт EmailVerification объект и отправляет письмо со ссылкой верификации полькозателю'''
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=48)  # дата и время, когда код будет считаться недействительнам
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    send_verification_email(record)


def change_parameter_of_the_user_object(user):
    ''' Изменяет параметр is_verified_email объекта User'''
    user.is_verified_email = True
    user.save()
