from celery import Celery

from .services.sending_news import send_news_email

app = Celery('tasks', broker='redis://127.0.0.1:6379')

@app.task
def send_news_task(news_id):
    """Отправляет письмо с запросом на опеку"""
    return send_news_email(news_id)
