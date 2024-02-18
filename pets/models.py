from django.db import models
from django.urls import reverse
from users.models import User
from pytils.translit import slugify
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
    image = models.ImageField(upload_to='product_images', verbose_name=u"Фото животного")
    category = models.ForeignKey(to=PetsCategory, on_delete=models.CASCADE, verbose_name=u"Вид животного")
    slug = models.SlugField(default='', null=True)
    needs = models.TextField(verbose_name=u"Нужды в настоящий момент", null=True)
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