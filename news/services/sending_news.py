from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from users.models import User
from pets.models import PetHistory, Basket
from ..models import News


def send_news_email(news_id):
    news = News.objects.get(pk=news_id)
    subject = news.title
    image = "http://127.0.0.1:8003/" + news.image.url
    data = {'news': news, 'image': image}
    html_body = render_to_string('news/news_email_template.html', data)
    users = User.objects.filter(common_news=True)
    email_list = [user.email for user in users]
    from_email = settings.EMAIL_HOST_USER
    message = EmailMessage(subject, html_body, from_email, email_list)
    message.content_subtype = 'html'  # this is required because there is no plain text email message
    message.send()


def send_pet_hystory_node(hystory_node_id):
    news = PetHistory.objects.get(pk=hystory_node_id)
    subject = news.title
    data = {'news': news}
    html_body = render_to_string('news/news_email_template.html', data)

    baskets = Basket.objects.filter(pet=news.pet)
    email_list = [basket.user.email for basket in baskets]
    from_email = settings.EMAIL_HOST_USER
    message = EmailMessage(subject, html_body, from_email, email_list)
    message.content_subtype = 'html'
    message.send()
