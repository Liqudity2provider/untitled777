import uuid
from django.contrib.auth.models import User
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase, URLPatternsTestCase


class AccountTests(APITestCase):
    CREATE_USER = {
        'username': str(uuid.uuid4()),
        'email': 'create@gmail.com',
        'password': "test_password",
        'password2': "test_password"
    }
    UPDATE_USER = {
        'username': str(uuid.uuid4()),
        'email': 'update@gmail.com',
        'password': "update_password",
        'password2': "update_password"
    }
    USER_WRONG_PASSWORD = {
        'username': str(uuid.uuid4()),
        'email': 'test2@gmail.com',
        'password': "first123",
        'password2': "first1234"
    }
    USER_SHORT_PASSWORD = {
        'username': str(uuid.uuid4()),
        'email': 'test2@gmail.com',
        'password': "first",
        'password2': "first"
    }
    USER_NUMBER_PASSWORD = {
        'username': str(uuid.uuid4()),
        'email': 'test2@gmail.com',
        'password': "555551111",
        'password2': "555551111"
    }
    USER_BLANK_USERNAME = {
        'username': '',
        'email': 'hgvh@gmail.com',
        'password': "first123",
        'password2': "first123"
    }

    def test_create_user(self):
        url = reverse('all-users')
        response = self.client.post(url, format='json', data=self.CREATE_USER)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_create_existing_user(self):
        url = reverse('all-users')
        self.client.post(url, format='json', data=self.CREATE_USER)
        response = self.client.post(url, format='json', data=self.CREATE_USER)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'username': [ErrorDetail(string='A user with that username already exists.', code='unique')]})
        self.assertEqual(User.objects.count(), 1)

    def test_create__username_validation(self):
        url = reverse('all-users')
        response = self.client.post(url, format='json', data=self.USER_BLANK_USERNAME)
        self.assertEqual(response.data,
                         {'username': [ErrorDetail(string='This field may not be blank.', code='blank')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create__password_validation(self):
        url = reverse('all-users')
        response = self.client.post(url, format='json', data=self.USER_WRONG_PASSWORD)
        self.assertEqual(response.data,
                         {'non_field_errors': [ErrorDetail(string='Passwords doesnt match', code='invalid')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create__password_validation_2(self):
        url = reverse('all-users')
        response = self.client.post(url, format='json', data=self.USER_SHORT_PASSWORD)
        self.assertEqual(response.data,
                         {'non_field_errors': [
                             ErrorDetail(string='This password is too short. It must contain at least 8 characters.',
                                         code='password_too_short')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create__password_validation_3(self):
        url = reverse('all-users')
        response = self.client.post(url, format='json', data=self.USER_NUMBER_PASSWORD)
        self.assertEqual(response.data,
                         {'non_field_errors': [ErrorDetail(string='This password is entirely numeric.',
                                                           code='password_entirely_numeric')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        url = reverse('all-users')
        self.client.post(url, format='json', data=self.CREATE_USER)
        url = reverse('user', kwargs={'pk': 1})
        response = self.client.put(url, format='json', data=self.UPDATE_USER)
        self.assertEqual(response.data.get('email'), "update@gmail.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_update_user__username_validation(self):
        url = reverse('all-users')
        self.client.post(url, format='json', data=self.CREATE_USER)
        url = reverse('user', kwargs={'pk': 1})
        response = self.client.put(url, format='json', data=self.USER_BLANK_USERNAME)
        self.assertEqual(response.data,
                         {'username': [ErrorDetail(string='This field may not be blank.', code='blank')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_update_user__password_validation(self):
        url = reverse('all-users')
        self.client.post(url, format='json', data=self.CREATE_USER)
        url = reverse('user', kwargs={'pk': 1})
        response = self.client.put(url, format='json', data=self.USER_WRONG_PASSWORD)
        self.assertEqual(response.data,
                         {'non_field_errors': [ErrorDetail(string='Passwords doesnt match', code='invalid')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_delete_user(self):
        url = reverse('all-users')
        self.client.post(url, format='json', data=self.CREATE_USER)
        url = reverse('user', kwargs={'pk': 1})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
