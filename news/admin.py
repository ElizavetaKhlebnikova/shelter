from django.contrib import admin

# Register your models here.
from .models import News, PetSubscriber

admin.site.register(News)
admin.site.register(PetSubscriber)
