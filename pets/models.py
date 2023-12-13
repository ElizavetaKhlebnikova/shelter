from django.db import models

from users.models import User

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


class Pet(models.Model):
    name = models.CharField(max_length=256, verbose_name=u"Кличка животного")
    description = models.TextField(verbose_name=u"Описание")
    image = models.ImageField(upload_to='product_images', verbose_name=u"Фото животного")
    category = models.ForeignKey(to=PetsCategory, on_delete=models.CASCADE, verbose_name=u"Вид животного")
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
        verbose_name = 'животное'
        verbose_name_plural = 'животные'
    def __str__(self):
        return f'Имя подопечного: {self.name} | Вид: {self.category}'


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    pet = models.ForeignKey(to=Pet, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)