import concurrent.futures
import threading

from django.forms import model_to_dict
from django.http import HttpResponse
from httplib2 import Response
from rest_framework import generics
from rest_framework.generics import get_object_or_404

from films.models import Film, Comment
from films.serializers import FilmSerializer, CommentSerializer


class FilmApiListView(generics.ListAPIView):
    """
    List all films
    """
    serializer_class = FilmSerializer
    model = Film

    @staticmethod
    def update_results_by_url_of_image(film, results):
        """
        Updating dict of image urls
        """
        if isinstance(film, Film):
            results.update({
                film.name: film.image.url
            })
        else:
            return results

    @staticmethod
    def return_urls_of_images_using_threading(query):
        """
        Because of getting url of image in operation of input-output(work with server),
        we need to make it more faster - using threads
        """

        thread_list = []
        results = {}
        for film in query:
            """
            take each film in list of Film objects
            and creating a Thread with function that gets url of image form server
            than adding thread in list of threads 
            """
            thread = threading.Thread(target=FilmApiListView.update_results_by_url_of_image, args=(film, results))
            thread_list.append(thread)
        for thread in thread_list:
            """
            Starting each thread with function that gets url of image from server
            """
            thread.start()
        for thread in thread_list:
            """
            We need wait for results of threads, so we should block flow
            """
            thread.join()
        return FilmApiListView.update_results_by_url_of_image(None, results)

    def get_queryset(self):
        """
        Get the list of items for this view.
        """

        list_of_films = []
        quer = list(Film.objects.all())

        genre_in_url = self.request.query_params.get('genre')
        if genre_in_url:
            quer = list(Film.objects.filter(genres__name=genre_in_url))

        for film in quer:
            f = model_to_dict(film)
            f.update({
                'genres': film.genres.all(),
                'comments': film.comments.all()
            })
            list_of_films.append(f)

        res = []

        url_images = self.return_urls_of_images_using_threading(quer)

        for film in list_of_films:
            film.update({
                'image_url': url_images.get(film.get('name'))
            })
            res.append(film)

        return res


class FilmApiDetailView(generics.RetrieveAPIView):
    serializer_class = FilmSerializer
    queryset = Film.objects.all()

    def get_object(self):
        """
        Returns the object the view is displaying.

        """
        quer = self.get_queryset()
        obj = get_object_or_404(quer, pk=self.kwargs.get('pk'))
        dict_obj = model_to_dict(obj)
        dict_obj.update({
            'genres': obj.genres.all(),
            'comments': obj.comments.all(),
            'image_url': obj.image.url,
        })

        return dict_obj


class CommentApiDetailView(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentApiListView(generics.ListCreateAPIView):
    """
        List all comments, or create a new.
        """
    queryset = Comment.objects.filter(deleted=False)
    serializer_class = CommentSerializer
