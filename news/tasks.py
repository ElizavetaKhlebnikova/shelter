from celery import Celery

from .services.sending_news import send_news_email
from .services.sending_news import send_pet_hystory_node

app = Celery('tasks', broker='redis://127.0.0.1:6379')

@app.task
def send_news_task(news_id):
    """Отправляет письмо с запросом на опеку"""
    return send_news_email(news_id)

@app.task
def send_pet_hystory_node_task(hystory_node_id):
    """Отправляет письмо с запросом на опеку"""
    return send_pet_hystory_node(hystory_node_id)
