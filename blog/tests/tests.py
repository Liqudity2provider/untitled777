# Create your tests here.
import uuid
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from blog.models import Post
from blog.tests.models_to_use_in_tests import CREATE_POST, CREATE_POST_WITHOUT_TITLE, CREATE_POST_WITHOUT_CONTENT, \
    UPDATE_POST
from users.utils import get_tokens_for_user, set_expiration_time_token


class PostTests(APITestCase):
    """
    Class testing Post rest API functionality
    """

    def setUp(self) -> None:
        self.user = User.objects.create_user(username=str(uuid.uuid4()))
        self.pair_tokens = get_tokens_for_user(self.user)
        self.token = self.pair_tokens['token']

    def test_get_post(self):
        """
        Testing GET request to existing Post
        """

        post = Post.objects.create(**CREATE_POST, author=self.user)
        url = reverse('api-post', kwargs={'pk': 1})

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual([response.data.get('author'), response.data.get('title'), response.data.get('content')], [
            self.user.username, post.title, post.content,
        ])

    def test_get_non_existing_post(self):
        """
        Testing GET request to not existing Post
        """

        post = Post.objects.create(**CREATE_POST, author=self.user)
        url = reverse('api-post', kwargs={'pk': 99})

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Not found.', code='not_found')})

    def test_create_post(self):
        """
        Testing POST request to create Post using JWT token auth
        """
        url = reverse('api-posts')

        response = self.client.post(url, data=CREATE_POST, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_create_using_expired_token_post(self):
        """
        Testing POST request to create Post using expired JWT token
        """

        url = reverse('api-posts')

        changed_exp_in_token = set_expiration_time_token(self.token, 1500000000)
        response = self.client.post(url, data=CREATE_POST, format='json',
                                    HTTP_AUTHORIZATION=f'Bearer {changed_exp_in_token}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)
        self.assertIn('token_not_valid', str(response.data))

    def test_create_post_validation_title(self):
        """
        Testing POST request to create Post without title (using JWT token auth)
        """

        url = reverse('api-posts')

        response = self.client.post(url, data=CREATE_POST_WITHOUT_TITLE, format='json',
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'title': [ErrorDetail(string='This field may not be blank.', code='blank')]})
        self.assertEqual(Post.objects.count(), 0)

    def test_create_post_validation_content(self):
        """
        Testing POST request to create Post without content (using JWT token auth)
        """

        url = reverse('api-posts')

        response = self.client.post(url, data=CREATE_POST_WITHOUT_CONTENT, format='json',
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'content': [ErrorDetail(string='This field may not be blank.', code='blank')]})
        self.assertEqual(Post.objects.count(), 0)

    def test_create_post_validation_auth(self):
        """
        Testing POST request to create Post without auth
        """

        url = reverse('api-posts')

        response = self.client.post(url, data=CREATE_POST_WITHOUT_CONTENT, format='json')

        self.assertEqual(response.data, {
            'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)

    def test_update_post(self):
        """
        Testing PUT request to update Post (using JWT token auth)
        """

        url = reverse('api-post', kwargs={'pk': 1})
        post = Post.objects.create(**CREATE_POST, author=self.user)

        response = self.client.put(url, data=UPDATE_POST, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get(pk=1).author, self.user)

    def test_update_post_validaton_title(self):
        """
        Testing PUT request to update Post without title (using JWT token auth)
        """

        post = Post.objects.create(**CREATE_POST, author=self.user)
        url = reverse('api-post', kwargs={'pk': 1})

        response = self.client.put(url, data=CREATE_POST_WITHOUT_TITLE, format='json',
                                   HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'title': [ErrorDetail(string='This field may not be blank.', code='blank')]})
        self.assertEqual(Post.objects.count(), 1)

    def test_update_post_validation_content(self):
        """
        Testing PUT request to update Post without content (using JWT token auth)
        """

        post = Post.objects.create(**CREATE_POST, author=self.user)
        url = reverse('api-post', kwargs={'pk': 1})

        response = self.client.put(url, data=CREATE_POST_WITHOUT_CONTENT, format='json',
                                   HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'content': [ErrorDetail(string='This field may not be blank.', code='blank')]})
        self.assertEqual(Post.objects.count(), 1)

    def test_update_post_validation_auth(self):
        """
        Testing PUT request to update Post without auth
        """

        post = Post.objects.create(**CREATE_POST, author=self.user)
        url = reverse('api-post', kwargs={'pk': 1})

        response = self.client.put(url, data=CREATE_POST_WITHOUT_CONTENT, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data,
                         {'detail': ErrorDetail(string='Authentication credentials were not provided.',
                                                code='not_authenticated')})
        self.assertEqual(Post.objects.count(), 1)

    def test_delete_post(self):
        """
        Testing DELETE request to delete Post (using JWT token auth)
        """

        post = Post.objects.create(**CREATE_POST, author=self.user)
        url = reverse('api-post', kwargs={'pk': 1})

        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(list(Post.objects.all()), [])

    def test_delete_non_existing_post(self):
        """
        Testing DELETE request to delete non existing Post (using JWT token auth)
        """

        post = Post.objects.create(**CREATE_POST, author=self.user)
        url = reverse('api-post', kwargs={'pk': 888})

        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), 1)

    def test_delete_post_by_another_user(self):
        """
        Testing DELETE request to delete Post by another user credentials (using JWT token auth)
        """

        user_2 = User.objects.create_user(username=uuid.uuid4(), password='password1029387')
        post = Post.objects.create(**CREATE_POST, author=user_2)
        url = reverse('api-post', kwargs={'pk': 1})

        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)
