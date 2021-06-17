from unittest.mock import Mock

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from films.fixtures import data
# Create your tests here.
from films.models import Film
from films.services import ServiceUpdateFilmList
from films.utils_parse import parse_func
from users.utils import get_tokens_for_user


class FilmTests(APITestCase):
    """
    Class testing Post rest API functionality
    """
    fixtures = ['fixtures.json']

    def test_delete_films(self):
        """
        Testing delete method for films
        """

        self.assertGreater(Film.objects.count(), 20)
        ServiceUpdateFilmList.delete_all_objects()
        self.assertEqual(Film.objects.count(), 0)

    def test_update_films(self):
        """
        Testing update method for films
        """

        ServiceUpdateFilmList.delete_all_objects()
        self.assertEqual(Film.objects.count(), 0)

        ServiceUpdateFilmList.get_data_from_parse_methods = Mock(return_value=(data.genres, data.films))

        list_genres, list_with_films = ServiceUpdateFilmList.get_data_from_parse_methods()

        ServiceUpdateFilmList.adding_genres_in_db_from_list(list_genres)

        ServiceUpdateFilmList.adding_films_in_db_from_list(list_with_films)

        url = reverse('api-films')

        token = get_tokens_for_user(User.objects.get(pk=1)).get('token')

        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(Film.objects.count(), len(list_with_films))
        self.assertIn('Доктор Лиза', str(response.data))

    def test_wrong_update_films(self):
        """
        Testing error update method for films
        """

        ServiceUpdateFilmList.delete_all_objects()
        self.assertEqual(Film.objects.count(), 0)

        ServiceUpdateFilmList.adding_genres_in_db_from_list({})
        ServiceUpdateFilmList.adding_films_in_db_from_list([])
