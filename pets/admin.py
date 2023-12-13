from django.contrib import admin

# Register your models here.
from .models import Basket, Pet, PetsCategory, PetStatus

admin.site.register(PetsCategory)
admin.site.register(PetStatus)

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'category', 'is_hospitalized', 'status')
    search_fields = ('name', )

class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('pet', )
    extra = 0