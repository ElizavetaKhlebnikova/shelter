from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Pet, PetsCategory, OtherPet, RequestForGuardianship

from unittest.mock import patch


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'pets/index.html')
        self.assertEqual(response.context_data['title'], 'HappyVeganShelter')


class DonationViewTestCase(TestCase):

    def test_view(self):
        path = reverse('pets:help')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'pets/donation.html')
        self.assertEqual(response.context_data['title'], 'HappyVeganShelter - моя помощь')


class PetListTestCase(TestCase):
    fixtures = ['pet_category.json', 'pet_status.json', 'pets.json']

    def setUp(self):
        self.paginate_by = 8

    def test_filter_by_category(self):
        data_len = len(Pet.objects.filter(category=1))
        page = left = 0
        right = self.paginate_by

        while data_len > 0:
            page += 1
            path = reverse('pets:index')
            response = self.client.get(path + f'?category=1&gender=-&status=-&page={page}')
            exp_response = Pet.objects.filter(category=1)
            self.assertQuerysetEqual(response.context_data.get('object_list'), exp_response[left:right],
                                     ordered=False)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateUsed(response, 'pets/pets.html')
            data_len -= self.paginate_by
            left = right
            right += self.paginate_by

    def test_filter_by_gender(self):
        data_len = len(Pet.objects.filter(gender='f'))
        page = left = 0
        right = self.paginate_by

        while data_len > 0:
            page += 1
            path = reverse('pets:index')
            response = self.client.get(path + f'?category=-&gender=f&status=-&page={page}')
            exp_response = Pet.objects.filter(gender='f')
            self.assertQuerysetEqual(response.context_data.get('object_list'), exp_response[left:right],
                                     ordered=False)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateUsed(response, 'pets/pets.html')
            data_len -= self.paginate_by
            left = right
            right += self.paginate_by

    def test_filter_by_status(self):
        data_len = len(Pet.objects.filter(status=2))
        page = left = 0
        right = self.paginate_by

        while data_len > 0:
            page += 1
            path = reverse('pets:index')
            response = self.client.get(path + f'?category=-&gender=-&status=2&page={page}')
            exp_response = Pet.objects.filter(status=2)
            self.assertQuerysetEqual(response.context_data.get('object_list'), exp_response[left:right],
                                     ordered=False)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateUsed(response, 'pets/pets.html')
            data_len -= self.paginate_by
            left = right
            right += self.paginate_by

    def test_category(self):
        category_id_list = [category.id for category in PetsCategory.objects.all()]

        for category_id in category_id_list:
            path = reverse('pets:index')
            response = self.client.get(path + f'?category={category_id}&gender=-&status=-')
            self.assertEqual(response.status_code, HTTPStatus.OK)
            if len(Pet.objects.filter(category_id=category_id)) / self.paginate_by > 1:
                self.assertTemplateUsed(response, 'pets/pets.html')
                self.assertTrue('is_paginated' in response.context)
                self.assertTrue(response.context['is_paginated'] == True)
                self.assertTrue(len(response.context['object_list']) == self.paginate_by)


class RequestForGuardianshipTestCase(TestCase):
    fixtures = ['pet_category.json', 'pet_status.json', 'pets.json', 'other_pet.json']

    def setUp(self):
        self.path = reverse('pets:guardianship', kwargs={'category_id': 1})
        other_pet = OtherPet.objects.all()
        self.data = {
            'user_name': 'Liza',
            'email': 'lizka-khlebnukova@yandex.ru',
            'pet': 'Эмми',
            'city': 'Санкт-Петербург',
            'goal': 'home',
            'other_pets': OtherPet.objects.all(),
            'other_pet': 'Шиншилла',
            'conditions': True
        }

    def test_request_for_guardianship_form_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'HappyVeganShelter - заявка на опеку')
        self.assertTemplateUsed(response, 'pets/request_for_guardianship_form.html')


