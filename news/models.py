from django.db import models
from pets.models import Pet
# Create your models here.

class News(models.Model):
    index_number = models.IntegerField(verbose_name=u"Порядок отображения*")
    title = models.CharField(max_length=60, verbose_name=u"Заголовок новости*")
    text = models.TextField(max_length=400, verbose_name=u"Текст новости*")
    image = models.ImageField(upload_to='news_images', verbose_name=u"Фото*")
    image_url = models.TextField(max_length=400, verbose_name=u"текст ссылки на картинку",  null=True, blank=True,)
    connection = models.BooleanField(default=False, verbose_name=u"Нужна ссылка на подопечного?")
    pet = models.ForeignKey(to=Pet, null=True, blank=True, on_delete=models.CASCADE,
                            verbose_name=u"Подопечный, на которого даётся ссылка")
    send_news = models.BooleanField(default=False, verbose_name=u"Отправить в почтовую рассылку")

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return f'Новость № {self.index_number}: {self.title}'

