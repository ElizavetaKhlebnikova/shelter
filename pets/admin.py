from django.contrib import admin

from .models import (Basket, OtherPet, Pet, PetHistory, PetImage,
                     PetsCategory, PetStatus, RequestForGuardianship)

admin.site.register(PetsCategory)
admin.site.register(PetStatus)
admin.site.register(PetHistory)
admin.site.register(PetImage)
admin.site.register(RequestForGuardianship)
admin.site.register(OtherPet)


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'category', 'is_hospitalized', 'status')
    search_fields = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('pet',)
    extra = 0
