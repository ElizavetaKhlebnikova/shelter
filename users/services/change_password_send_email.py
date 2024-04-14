from django.conf import settings
from django.core.mail import send_mail



def send_email_about_change_password(email):
    """Генерирует текст письма с информацией о смене пароля"""
    subject = 'Вы сменили пароль'
    message = 'Уважаемый пользователь, вы успешно сменили пароль на нашеи сайте!'
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
