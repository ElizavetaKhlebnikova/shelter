from celery import Celery

from .services.sending_email import send_email_about_request_for_guardianship

app = Celery('tasks', broker='redis://127.0.0.1:6379')

@app.task
def send_email_about_request_for_guardianship_task(request_pk):
    return send_email_about_request_for_guardianship(request_pk)
