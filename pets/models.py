from django.db import models
from django.urls import reverse
from users.models import User
from pytils.translit import slugify
from django.core.mail import send_mail
from django.conf import settings
# Create your models here.

class PetsCategory(models.Model):
    name = models.CharField(max_length=128)
    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'категории'
    def __str__(self):
        return self.name


class PetStatus(models.Model):
    status = models.CharField(max_length=128)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Статус подопечного'
        verbose_name_plural = 'Статусы подопечных'


class Pet(models.Model):
    name = models.CharField(max_length=256, verbose_name=u"Кличка животного")
    description = models.TextField(verbose_name=u"Описание")
    image = models.ImageField(upload_to='pet_images', verbose_name=u"Фото животного", null=True, blank=True,)
    category = models.ForeignKey(to=PetsCategory, on_delete=models.CASCADE, verbose_name=u"Вид животного")
    slug = models.SlugField(default='', null=True, blank=True,)
    needs = models.TextField(verbose_name=u"Нужды в настоящий момент", null=True, blank=True,)
    MALE = 'm'
    FEMALE = 'f'
    GENDERS = [
        (MALE, 'Мальчик'),
        (FEMALE, 'Девочка')
    ]
    is_hospitalized = models.BooleanField(default=False, verbose_name=u"Находится в стационаре")
    gender = models.CharField(max_length=1, choices=GENDERS, default=MALE, verbose_name=u"Пол животного")
    status = models.ForeignKey(to=PetStatus, on_delete=models.CASCADE, verbose_name=u"Статус")

    class Meta:
        verbose_name = 'подопечный'
        verbose_name_plural = 'Подопечные'
    def __str__(self):
        return f'Имя подопечного: {self.name} | Вид: {self.category}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    pet = models.ForeignKey(to=Pet, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)

class PetHistory(models.Model):
    pet = models.ForeignKey(to=Pet, on_delete=models.CASCADE, verbose_name=u"Кличка подопечного")
    time = models.DateField(auto_now_add=False, verbose_name=u"Дата")
    node = models.TextField(verbose_name=u"Новость из жизни подопечного")
    class Meta:
        verbose_name = 'История подопечного'
        verbose_name_plural = 'Истории подопечных'
    def __str__(self):
        return f'Событие из жизни подопечного: {self.pet.name} | Дата: {self.time}'

class PetImage(models.Model):
    pet = models.ForeignKey(to=Pet, on_delete=models.CASCADE, verbose_name=u"Кличка подопечного")
    image = models.ImageField(upload_to='pet_images', verbose_name=u"Фото животного")
    index_number = models.IntegerField(verbose_name=u"Порядок отображения")
    class Meta:
        verbose_name = 'Фотография подопечного'
        verbose_name_plural = 'Фотогафии подопечных'
    def __str__(self):
        return f'Фотография подопечного: {self.pet.name}'

class News(models.Model):
    index_number = models.IntegerField(verbose_name=u"Порядок отображения")
    title = models.CharField(max_length=60, verbose_name=u"Заголовок новости")
    text = models.TextField(max_length=400, verbose_name=u"Текст новости")
    image = models.ImageField(upload_to='news_images', verbose_name=u"Фото")
    connection = models.BooleanField(default=False, verbose_name=u"Нужна ссылка на подопечного?")
    pet = models.ForeignKey(to=Pet, null=True, blank=True, on_delete=models.CASCADE, verbose_name=u"Подопечный, на которого даётся ссылка")


    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
    def __str__(self):
        return f'Новость № {self.index_number}: {self.title}'

class OtherPets(models.Model):
    pets = models.CharField(max_length=20, verbose_name=u"Вид животного")

    def __str__(self):
        return self.pets

class RequestForGuardianship(models.Model):
    user_name = models.CharField(max_length=256, verbose_name=u"Имя пользователя")
    email = models.EmailField(unique=True, verbose_name=u"Электронная почта для связи")
    pet = models.CharField(max_length=256, verbose_name=u"Кличка подопечного")
    city = models.CharField(max_length=256, verbose_name=u"Город проживания")
    created = models.DateTimeField(auto_now_add=True)
    goals = (
        ('None', 'не выбрано'),
        ('foster care', 'передержка'),
        ('home', 'дом')
    )
    goal = models.CharField(max_length=20, choices=goals, verbose_name=u"Кем вы готовы стать для животного?")
    other_pets = models.ManyToManyField(to=OtherPets, verbose_name=u"Если у вас уже есть питомцы, укажите, какие:")
    other_pet = models.CharField(max_length=256, verbose_name=u"Укажите вид вашего питомца", null=True, blank=True)
    conditions = models.BooleanField(verbose_name=u"Готовы ли вы выполнить все условия?")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        subject = 'У вас новая заявка на опеку'
        message = 'Дата создания обращения: {}\nПользователь: {}\nEmail: {}\nГород: {}\nЦель запроса: {}\nПитомец: {}\nГотовность выполнения условий: {}'.format(
            self.created,
            self.user_name,
            self.email,
            self.city,
            {'None': 'не выбрано', 'foster care': 'передержка', 'home': 'дом'}[self.goal],
            self.pet,
            {False: "не готов", True: "готов"}[self.conditions]
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['lizka-khlebnikova@yandex.ru'],
            fail_silently=False,
        )
