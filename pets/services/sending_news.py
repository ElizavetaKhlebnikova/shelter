from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from ..models import User


def send_news_email(news):
    subject = news.title
    image = "http://127.0.0.1:8003/" + news.image.url
    data = {'news': news, 'image': image}
    html_body = render_to_string('pets/common_news.html', data)
    users = User.objects.filter(common_news=True)
    email_list = [user.email for user in users]
    from_email = settings.EMAIL_HOST_USER
    message = EmailMessage(subject, html_body, from_email, email_list)
    message.content_subtype = 'html'  # this is required because there is no plain text email message
    message.send()