from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Pet, PetsCategory


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'pets/index.html')
        self.assertEqual(response.context_data['title'], 'HappyVeganShelter')

class PetListTestCase(TestCase):
    fixtures = ['pet_category.json', 'pet_status.json', 'pets.json']

    def setUp(self):
        self.paginate_by = 3

    def test_list(self):
        page = left = 0
        right = self.paginate_by
        data_len = len(Pet.objects.all())

        while data_len > 0:
            page += 1
            path = reverse('pets:paginator', kwargs={'page': page})
            response = self.client.get(path)
            self.assertQuerysetEqual(response.context_data.get('object_list'), Pet.objects.all()[left:right], ordered=False)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateUsed(response, 'pets/pets.html')
            data_len -= self.paginate_by
            left = right
            right += self.paginate_by

    def test_category(self):

        for category in range(1, len(PetsCategory.objects.order_by('id').all()) + 1):
            path = reverse('pets:category', kwargs={'category_id': category})
            response = self.client.get(path)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            if len(Pet.objects.filter(category_id=category)) / self.paginate_by > 1:
                self.assertTemplateUsed(response, 'pets/pets.html')
                self.assertTrue('is_paginated' in response.context)
                self.assertTrue(response.context['is_paginated'] == True)
                self.assertTrue(len(response.context['object_list']) == self.paginate_by)




