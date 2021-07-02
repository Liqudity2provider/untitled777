import concurrent.futures
import threading

from django.forms import model_to_dict
from django.http import HttpResponse
from rest_framework import generics

from films.models import Film, Comment
from films.serializers import FilmSerializer, CommentSerializer


class FilmApiDetailView(generics.RetrieveUpdateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


class FilmApiListView(generics.ListCreateAPIView):
    """
        List all posts, or create a new.
        """
    serializer_class = FilmSerializer
    model = Film

    @staticmethod
    def func_thread(film, results):
        """
        Updating dict of image urls
        """
        if film:
            results.update({
                film.name: film.image.url
            })
        else:
            return results

    def return_urls_of_images_using_threading(self, query):
        """
        Because of getting url of image in operation of input-output(work with server),
        we need to make it more faster - using threads
        """
        thread_list = []
        results = {}
        for film in query:
            thread = threading.Thread(target=self.func_thread, args=(film, results))
            thread_list.append(thread)
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()
        return self.func_thread(None, results)

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


class CommentApiDetailView(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentApiListView(generics.ListCreateAPIView):
    """
        List all comments, or create a new.
        """
    queryset = Comment.objects.filter(deleted=False)
    serializer_class = CommentSerializer
