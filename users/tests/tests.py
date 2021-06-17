import re
import time
import uuid

import pytest
import jwt
from django.contrib.auth.models import User
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase, URLPatternsTestCase
from users.tests.test_fixtures import CREATE_USER, UPDATE_USER, USER_BLANK_USERNAME, USER_NUMBER_PASSWORD, \
    USER_SHORT_PASSWORD, USER_WRONG_PASSWORD
import core.settings
from core import settings
from users.utils import check_expiration, set_expiration_time_token, get_tokens_for_user


class AccountTests(APITestCase):
    """
    Class testing User rest API functionality
    """
    fixtures = ['fixtures.json']

    def test_get_user(self, ):
        """
        Testing GET request to existing User
        """

        url = reverse('user', kwargs={'pk': 1})
        user = User.objects.get(pk=1)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual([response.data.get('username'), response.data.get('email')], [
            user.username, user.email,
        ])

    def test_get_non_existing_user(self):
        """
        Testing GET request to not existing User
        """

        url = reverse('user', kwargs={'pk': 8888})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Not found.', code='not_found')})

    def test_create_user(self):
        """
        Testing POST request to create User
        """

        url = reverse('all-users')
        response = self.client.post(url, format='json', data=CREATE_USER)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_existing_user(self):
        """
        Testing POST request to create existing User
        """

        url = reverse('all-users')
        self.client.post(url, format='json', data=CREATE_USER)
        response = self.client.post(url, format='json', data=CREATE_USER)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'username': [ErrorDetail(string='A user with that username already exists.', code='unique')]})

    def test_create__username_validation(self):
        """
        Testing POST request to create User without username
        """

        url = reverse('all-users')
        response = self.client.post(url, format='json', data=USER_BLANK_USERNAME)
        self.assertEqual(response.data,
                         {'username': [ErrorDetail(string='This field may not be blank.', code='blank')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create__password_validation(self):
        """
        Testing POST request to create User with passwords that doesnt match
        """

        url = reverse('all-users')
        response = self.client.post(url, format='json', data=USER_WRONG_PASSWORD)
        self.assertEqual(response.data,
                         {'non_field_errors': [ErrorDetail(string='Passwords doesnt match', code='invalid')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create__password_validation_2(self):
        """
        Testing POST request to create User with bad passwords
        """

        url = reverse('all-users')
        response = self.client.post(url, format='json', data=USER_SHORT_PASSWORD)
        self.assertEqual(response.data,
                         {'non_field_errors': [
                             ErrorDetail(string='This password is too short. It must contain at least 8 characters.',
                                         code='password_too_short')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create__password_validation_3(self):
        """
        Testing POST request to create User with bad passwords
        """

        url = reverse('all-users')
        response = self.client.post(url, format='json', data=USER_NUMBER_PASSWORD)
        self.assertEqual(response.data,
                         {'non_field_errors': [ErrorDetail(string='This password is entirely numeric.',
                                                           code='password_entirely_numeric')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        """
        Testing PUT request to update User
        """
        url = reverse('user', kwargs={'pk': 1})
        response = self.client.put(url, format='json', data=UPDATE_USER)
        self.assertEqual(response.data.get('email'), "update@gmail.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user__username_validation(self):
        """
        Testing PUT request to update User without username
        """

        url = reverse('all-users')
        self.client.post(url, format='json', data=CREATE_USER)
        url = reverse('user', kwargs={'pk': 1})
        response = self.client.put(url, format='json', data=USER_BLANK_USERNAME)
        self.assertEqual(response.data,
                         {'username': [ErrorDetail(string='This field may not be blank.', code='blank')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user__password_validation(self):
        """
        Testing PUT request to update User without password
        """

        url = reverse('all-users')
        self.client.post(url, format='json', data=CREATE_USER)
        url = reverse('user', kwargs={'pk': 1})
        response = self.client.put(url, format='json', data=USER_WRONG_PASSWORD)
        self.assertEqual(response.data,
                         {'non_field_errors': [ErrorDetail(string='Passwords doesnt match', code='invalid')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user(self):
        """
        Testing DELETE request to delete User
        """

        url = reverse('all-users')
        self.client.post(url, format='json', data=CREATE_USER)
        url = reverse('user', kwargs={'pk': 1})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TokenTests(APITestCase):
    """
    Class testing Token rest API functionality
    """
    fixtures = ['fixtures.json']

    def test_create_token(self):
        """
        Testing POST request to create Token for User
        """

        user = User.objects.create(username=str(uuid.uuid4()))
        user.set_password('test_password')
        user.save()

        data = {
            "username": user.username,
            "password": 'test_password',
        }
        url = reverse('token_obtain_pair')

        response = self.client.post(url, format='json', data=data)
        refresh, token = response.data.get('refresh'), response.data.get('access')
        assert re.match('[A-Za-z0-9_-]+', token)
        assert re.match('[A-Za-z0-9_-]+', refresh)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_decoding_encoding_token(self):
        """
        Get user and 2 tokens from method and check encoding and decoding of token
        """
        user = User.objects.get(pk=1)
        refresh = get_tokens_for_user(user).get('refresh')
        decoded = jwt.decode(refresh, options={"verify_signature": False})
        encoded = jwt.encode(decoded, key=core.settings.SECRET_KEY)
        self.assertEqual(encoded, refresh)
        self.assertEqual(User.objects.count(), 1)

    def test_expiration_token(self):
        """
        Get user and 2 tokens from method
        Changing expiration of tokens to EXPIRED using special method
        checking token expiration using special method
        asserting result from special method and what we waiting for
        """
        user = User.objects.get(pk=1)
        pair_tokens = get_tokens_for_user(user)
        changed_exp_in_token = set_expiration_time_token(pair_tokens.get('token'), 1500000000)
        changed_exp_in_refresh = set_expiration_time_token(pair_tokens.get('refresh'), 1500000000)

        result_of_checking = check_expiration(token=changed_exp_in_token, refresh=changed_exp_in_refresh)
        self.assertEqual(result_of_checking, {
            'error': 'token has been expired'
        })
        self.assertEqual(User.objects.count(), 1)

    def test_date_of_expire(self):
        """
        Get user and 2 tokens from method
        Getting time of token expiration from it payload
        Getting time of token expiration using settings and aggregating now time and difference
        Checking that time expiration of token matches with settings values
        """
        user = User.objects.get(pk=1)
        pair_tokens = get_tokens_for_user(user)

        token = pair_tokens['token']

        time_exp_token = jwt.decode(token, options={"verify_signature": False}).get('exp')
        time_when_should_expire = (time.time() + settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME').total_seconds())
        time_should_exp_after = time_when_should_expire - 60
        time_should_exp_before = time_when_should_expire + 60
        self.assertGreater(time_exp_token, time_should_exp_after)
        self.assertLess(time_exp_token, time_should_exp_before)
