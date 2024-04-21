from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from users.models import User
from pets.models import PetHistory
from ..models import News, PetSubscriber



def send_news_email(news_id):
    news = News.objects.get(pk=news_id)
    subject = news.title
    image = "http://127.0.0.1:8003/" + news.image.url
    data = {'news': news, 'image': image}
    html_body = render_to_string('news/news_email_template.html', data)
    users = User.objects.filter(common_news=True)
    email_list = [user.email for user in users]

    for email in email_list:
        data['user_email'] = email
        to_email = [email]
        from_email = settings.EMAIL_HOST_USER
        html_body = render_to_string('news/news_email_template.html', data)
        message = EmailMessage(subject, html_body, from_email, to_email)
        message.content_subtype = 'html'
        message.send()


def send_pet_hystory_node(hystory_node_id):
    news = PetHistory.objects.get(pk=hystory_node_id)
    subject = news.title
    data = {'news': news}

    pet_subscribers = PetSubscriber.objects.filter(pet=news.pet)
    email_list = [pet_subscriber.user.email for pet_subscriber in pet_subscribers]

    for email in email_list:
        data['user_email'] = email
        to_email = [email]
        from_email = settings.EMAIL_HOST_USER
        html_body = render_to_string('news/news_email_template.html', data)
        message = EmailMessage(subject, html_body, from_email, to_email)
        message.content_subtype = 'html'
        message.send()
