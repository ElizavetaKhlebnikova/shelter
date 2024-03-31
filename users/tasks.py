# from celery import Celery
# from users.models import User, EmailVerification
# import uuid
# from datetime import timedelta
#
# from django.utils.timezone import now
#
# app = Celery('tasks', broker='redis://127.0.0.1:6379')
#
# @app.task
# def send_email_verification(user_id):
#     user = User.objects.get(id=user_id)
#     expiration = now() + timedelta(hours=48)  # дата и время, когда код будет считаться недействительнам
#     record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
#     # uuid.uuid4() - метод создания уникального uuid объекта
#     record.send_verification_email()