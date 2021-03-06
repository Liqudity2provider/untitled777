import os
import urllib
from abc import ABC

from django.core.files import File
from django.db import IntegrityError, OperationalError, DatabaseError
from django.db.transaction import TransactionManagementError
from service_objects.services import Service
import urllib.request
from films import utils_parse
from films.forms import NewCommentForm
from films.models import Genre, Film


class ServiceUpdateFilmList(Service):

    def process(self):

        set_genres, list_with_films = self.get_data_from_parse_methods()

        self.adding_genres_in_db_from_list(set_genres)

        self.adding_films_in_db_from_list(list_with_films)
        return True

    @staticmethod
    def adding_films_in_db_from_list(list_with_films):
        for film in list_with_films:
            if not Film.objects.filter(name__contains=film['name']):
                url = film['image']
                new_film = Film(name=film['name'], link=film['link'], image=film['image'],
                                rating=film['rating'], )
                result = urllib.request.urlretrieve(url)

                new_film.image.save(
                    os.path.basename(url),
                    File(open(result[0], 'rb'))
                )

                new_film.save()

                for genre in film['genres']:

                    genre = Genre.objects.filter(name__contains=genre).first()
                    new_film.genres.add(genre)
                    new_film.save()

    @staticmethod
    def adding_genres_in_db_from_list(list_genres):
        for genre in list_genres:
            try:
                if not Genre.objects.filter(name__contains=genre):
                    new_genre = Genre(name=genre)
                    new_genre.save()

            except IntegrityError:
                # handling errors when adding objects to db
                pass

    @staticmethod
    def get_data_from_parse_methods():
        set_genres = utils_parse.return_genres()
        list_with_films = utils_parse.parse_func()
        return set_genres, list_with_films

    @staticmethod
    def delete_all_objects():
        Genre.objects.all().delete()
        Film.objects.all().delete()


class ServiceFilmDetailView(Service):

    def process(self):
        film_to_show = Film.objects.get(pk=self.data['pk'])
        comment_form = NewCommentForm()

        context = {
            'object': film_to_show,
            'comments': film_to_show.comments.filter(deleted=False),
            'comment_form': comment_form,
        }
        return context


class AddNewComment(Service):

    def process(self):
        pk = self.data['pk']
        request = self.data['request']
        film_to_show = Film.objects.get(pk=pk)
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.film = Film.objects.get(pk=pk)
            user_comment.author = request.user
            user_comment.save()

            comment_form = NewCommentForm()

            context = {
                'object': film_to_show,
                'comments': film_to_show.comments.filter(deleted=False),
                'comment_form': comment_form,
            }
            return {
                'status': True,
                'context': context,
            }
        return {
            'status': False,
            'context': None,
        }
