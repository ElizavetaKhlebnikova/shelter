from ..models import Pet, Basket


def create_or_update_the_basket(pet_id, user):
    """Проверяет наличие питомца в корзине пользователя и при его отсутствии добавляет питомца"""
    pet = Pet.objects.get(id=pet_id)
    basket = Basket.objects.filter(user=user, pet=pet)
    if not basket.exists():
        obj = basket.create(user=user, pet=pet)
        new = True
    else:
        obj = basket.first()
        new = False
    return obj, new
