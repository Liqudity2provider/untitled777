import json
from http.cookies import SimpleCookie

import requests
from django.test import TestCase

# Create your tests here.
import uuid
from django.contrib.auth.models import User
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase, URLPatternsTestCase

from blog.models import Post
from users.utils import get_tokens_for_user


def create_user_return_token_and_url_api_posts(name_url):
    url = reverse(name_url)
    user = User.objects.create_user(username=str(uuid.uuid4()), password='test1d234')
    pair_tokens = get_tokens_for_user(user)
    token = pair_tokens.get('token')
    return token, url, user


class PostTests(APITestCase):
    CREATE_POST = {
        "title": "Some title",
        "content": "Some content",
    }
    CREATE_POST_WITHOUT_TITLE = {
        "title": "",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut "
                   "labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris "
                   "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit"
                   " esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, "
                   "sunt in culpa qui officia deserunt mollit anim id est laborum",
    }

    CREATE_POST_WITHOUT_CONTENT = {
        "title": "Lorem",
        "content": "",
    }
    UPDATE_POST = {
        "title": "Update",
        "content": "Update",
    }

    def test_get_post(self):
        token, url, user = create_user_return_token_and_url_api_posts('api-posts')

        post = Post.objects.create(**self.CREATE_POST, author=user)
        url = reverse('api-post', kwargs={'pk': 1})

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual([response.data.get('author'), response.data.get('title'), response.data.get('content')], [
            user.username, 'Some title', 'Some content',
        ])

    def test_get_non_existing_post(self):
        token, url, user = create_user_return_token_and_url_api_posts('api-posts')

        post = Post.objects.create(**self.CREATE_POST, author=user)
        url = reverse('api-post', kwargs={'pk': 99})

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Not found.', code='not_found')})

    def test_create_post(self):
        token, url, user = create_user_return_token_and_url_api_posts('api-posts')

        response = self.client.post(url, data=self.CREATE_POST, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_create_post_validaton_title(self):
        token, url, user = create_user_return_token_and_url_api_posts('api-posts')

        response = self.client.post(url, data=self.CREATE_POST_WITHOUT_TITLE, format='json',
                                    HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'title': [ErrorDetail(string='This field may not be blank.', code='blank')]})
        self.assertEqual(Post.objects.count(), 0)

    def test_create_post_validation_content(self):
        token, url, user = create_user_return_token_and_url_api_posts('api-posts')

        response = self.client.post(url, data=self.CREATE_POST_WITHOUT_CONTENT, format='json',
                                    HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'content': [ErrorDetail(string='This field may not be blank.', code='blank')]})
        self.assertEqual(Post.objects.count(), 0)

    def test_create_post_validation_auth(self):
        url = reverse('api-posts')

        response = self.client.post(url, data=self.CREATE_POST_WITHOUT_CONTENT, format='json')

        self.assertEqual(response.data, {
            'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)

    def test_update_post(self):
        token, url, user = create_user_return_token_and_url_api_posts('api-posts')
        url = reverse('api-post', kwargs={'pk': 1})
        post = Post.objects.create(**self.CREATE_POST, author=user)

        response = self.client.put(url, data=self.UPDATE_POST, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get(pk=1).author, user)

    def test_update_post_validaton_title(self):
        token, url, user = create_user_return_token_and_url_api_posts('api-posts')
        post = Post.objects.create(**self.CREATE_POST, author=user)
        url = reverse('api-post', kwargs={'pk': 1})

        response = self.client.put(url, data=self.CREATE_POST_WITHOUT_TITLE, format='json',
                                   HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'title': [ErrorDetail(string='This field may not be blank.', code='blank')]})
        self.assertEqual(Post.objects.count(), 1)

    def test_update_post_validation_content(self):
        token, url, user = create_user_return_token_and_url_api_posts('api-posts')
        post = Post.objects.create(**self.CREATE_POST, author=user)
        url = reverse('api-post', kwargs={'pk': 1})

        response = self.client.put(url, data=self.CREATE_POST_WITHOUT_CONTENT, format='json',
                                   HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'content': [ErrorDetail(string='This field may not be blank.', code='blank')]})
        self.assertEqual(Post.objects.count(), 1)

    def test_update_post_validation_auth(self):
        token, url, user = create_user_return_token_and_url_api_posts('api-posts')

        post = Post.objects.create(**self.CREATE_POST, author=user)
        url = reverse('api-post', kwargs={'pk': 1})

        response = self.client.put(url, data=self.CREATE_POST_WITHOUT_CONTENT, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data,
                         {'detail': ErrorDetail(string='Authentication credentials were not provided.',
                                                code='not_authenticated')})
        self.assertEqual(Post.objects.count(), 1)

    def test_delete_post(self):
        token, url, user = create_user_return_token_and_url_api_posts('api-posts')

        post = Post.objects.create(**self.CREATE_POST, author=user)
        url = reverse('api-post', kwargs={'pk': 1})

        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(list(Post.objects.all()), [])

    def test_delete_non_existing_post(self):
        token, url, user = create_user_return_token_and_url_api_posts('api-posts')

        post = Post.objects.create(**self.CREATE_POST, author=user)
        url = reverse('api-post', kwargs={'pk': 888})

        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), 1)

    def test_delete_post_by_another_user(self):
        token, url, user = create_user_return_token_and_url_api_posts('api-posts')
        user_2 = User.objects.create_user(username=uuid.uuid4(), password='password1029387')
        post = Post.objects.create(**self.CREATE_POST, author=user_2)
        url = reverse('api-post', kwargs={'pk': 1})

        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)
