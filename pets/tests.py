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
        #IndexViewTestCase.test_view


class PetListTestCase(TestCase):
    fixtures = ['pet_category.json', 'pet_status.json', 'pets.json']

    def setUp(self):
        self.paginate_by = 9

    # def test_list(self):
    #     path = reverse('pets:index')
    #     response = self.client.get(path)
    #     self.assertEqual(response, response)
    #
    # def test_filter_by_category(self):
    #     data_len = len(Pet.objects.filter(category=1))
    #     page = left = 0
    #     right = self.paginate_by
    #     response = self.client.get(reverse('pets:index'), kwargs={'category': '1'})
    #     exp_response = Pet.objects.filter(category=1)
    #     self.assertQuerysetEqual(response.context_data.get('object_list'), exp_response,
    #                              ordered=False)
    #
    #     while data_len > 0:
    #         page += 1
    #         response = self.client.get(reverse('pets:index'), kwargs={'category_id': '1', 'page': page})
    #         exp_response = Pet.objects.filter(category=1)[left:right]
    #         self.assertQuerysetEqual(response.context_data.get('object_list'), exp_response,
    #                                  ordered=False)
    #         self.assertEqual(response.status_code, HTTPStatus.OK)
    #         self.assertTemplateUsed(response, 'pets/pets.html')
    #         data_len -= self.paginate_by
    #         left = right
    #         right += self.paginate_by
    #
    # def test_filter_by_gender(self):
    #     path = reverse('pets:index')
    #     response = self.client.get(path + '?category=-&gender=m&status=-')
    #     # Проверьте, соответствуют ли результаты заданному фильтру по полу.
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #
    # def test_filter_by_status(self):
    #     response = self.client.get(reverse('pets:index'), kwargs={'status': '1'})
    #     # Проверьте, соответствуют ли результаты заданному фильтру по статусу.
    #     self.assertTrue('условие проверки')

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
