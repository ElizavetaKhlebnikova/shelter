from celery import Celery
from .services.send_verification_email import create_email_verification_object

from django.utils.timezone import now

app = Celery('tasks', broker='redis://127.0.0.1:6379')

@app.task
def send_email_verification(user_id):
    create_email_verification_object(user_id)