from django.conf import settings
from users.models import User, EmailVerification
import uuid
from datetime import timedelta

def send_verification_email(record):
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

def create_email_verification_object(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=48)  # дата и время, когда код будет считаться недействительнам
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    send_verification_email(record)