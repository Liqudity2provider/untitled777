import time
from collections import OrderedDict
from datetime import datetime
from unittest.mock import Mock
from django.test import RequestFactory

from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from films.api import FilmApiListView, FilmApiDetailView
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

    def test_wrong_update_films(self):
        """
        Testing error update method for films
        """

        ServiceUpdateFilmList.delete_all_objects()
        self.assertEqual(Film.objects.count(), 0)

        ServiceUpdateFilmList.adding_genres_in_db_from_list({})
        ServiceUpdateFilmList.adding_films_in_db_from_list([])

    def test_wrong_update_films_2(self):
        """
        Testing error update method for films
        """

        self.assertRaises(TypeError, ServiceUpdateFilmList.adding_genres_in_db_from_list([1, 2]))

    def test_get_films_data(self):
        url = reverse('api-films')
        response = self.client.get(url, format='json')
        self.assertGreater(Film.objects.count(), 20)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data[0]), OrderedDict)

    def test_get_film_data(self):
        film = Film.objects.all().first()
        url = reverse('api-film', kwargs={'pk': film.pk})
        response = self.client.get(url, format='json')
        self.assertGreater(Film.objects.count(), 20)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_wrong_film_data(self):
        url = reverse('api-film', kwargs={'pk': 99999999})
        response = self.client.get(url, format='json')
        self.assertGreater(Film.objects.count(), 20)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_results_by_url_of_image(self):
        results = dict()
        film_first = Film.objects.first()
        FilmApiListView.update_results_by_url_of_image(film=film_first, results=results)
        results = FilmApiListView.update_results_by_url_of_image(film=None, results=results)
        self.assertIn('dropbox', results[film_first.name])

    def test_wrong_update_results_by_url_of_image(self):
        results = dict()
        results = FilmApiListView.update_results_by_url_of_image(film=['efe'], results=results)
        self.assertEqual(results, dict())

    def test_time_return_urls_of_images_using_threading(self):
        quer = Film.objects.all()

        start_time_2 = datetime.now()

        res = FilmApiListView.return_urls_of_images_using_threading(quer)

        end_time_2 = datetime.now()
        duration = (end_time_2 - start_time_2).total_seconds()

        self.assertLess(duration, 3)

    def test_wrong_type_return_urls_of_images_using_threading(self):
        wrong_quer = 123456789
        self.assertRaises(TypeError, FilmApiListView.return_urls_of_images_using_threading, args=wrong_quer)

    def test_get_queryset_from_view(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        view = FilmApiListView.as_view()
        response = view(request)
        list_films = response.data
        self.assertEqual(len(list_films), Film.objects.count())
        self.assertIn('image_url', str(list_films))

    def test_get_queryset_from_class(self):
        request = RequestFactory().get('/')
        request.query_params = dict()
        view = FilmApiListView()
        view.request = request

        qs = view.get_queryset()
        self.assertEqual(len(qs), Film.objects.count())
        self.assertIn('image_url', str(qs))

    def test_get_object_from_class(self):
        request = RequestFactory().get('/')
        view = FilmApiDetailView()
        view.kwargs = {'pk': Film.objects.first().pk}
        view.request = request

        obj = view.get_object()
        self.assertIn('image_url', str(obj))
