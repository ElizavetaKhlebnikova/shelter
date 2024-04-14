from celery import Celery

from .services.verification import create_and_send_email_verification_object
from .services.change_password_send_email import send_email_about_change_password

app = Celery('tasks', broker='redis://127.0.0.1:6379')


@app.task
def send_email_verification(user_id):
    """Отправляет письмо верификации пользователю"""
    create_and_send_email_verification_object(user_id)

@app.task
def send_email_about_change_password_task(email):
    """Отправляет письмо о смене пароля пользователю"""
    send_email_about_change_password(email)
