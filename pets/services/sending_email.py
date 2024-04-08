from django.conf import settings
from django.core.mail import send_mail

from ..models import RequestForGuardianship


def send_email_about_request_for_guardianship(request_pk):
    request_for_guardianship = RequestForGuardianship.objects.get(pk=request_pk)
    subject = 'У вас новая заявка на опеку'
    message = 'Дата создания обращения: {}\nПользователь: {}\nEmail: {}\nГород: {}\nЦель запроса: {}\nПитомец: {}\nГотовность выполнения условий: {}'.format(
        request_for_guardianship.created,
        request_for_guardianship.user_name,
        request_for_guardianship.email,
        request_for_guardianship.city,
        {'None': 'не выбрано', 'foster care': 'передержка', 'home': 'дом'}[request_for_guardianship.goal],
        request_for_guardianship.pet,
        {False: "не готов", True: "готов"}[request_for_guardianship.conditions]
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['lizka-khlebnikova@yandex.ru'],
        fail_silently=False,
    )
