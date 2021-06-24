import json
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from films.models import Film, Genre
from films.services import ServiceUpdateFilmList, ServiceFilmDetailView, AddNewComment
from users.utils import refresh_token_or_redirect, user_from_token


class FilmsMainPage(APIView):

    def get(self, request, **kwargs):
      
        """:return films filtered by Genre name"""
        token = refresh_token_or_redirect(request)

        if not isinstance(token, str):
            return redirect('logout')

        contex = {
            'data_films': Film.objects.all(),
            'genres': Genre.objects.all(),
            'user': user_from_token(token),
        }
        if kwargs.get('params'):
            contex['data_films'] = Film.objects.filter(genres__name=kwargs.get('params'))

        return render(request, 'film/index.html', contex)


class UpdateFilmList(CreateView):
    """delete films, genres and comments. Parse and adds from site"""

    def get(self, request, **kwargs):
        status_ubdatedb = ServiceUpdateFilmList.execute({})

        if status_ubdatedb:
            return render(request, 'film/done.html', {})
        return HttpResponseNotFound('Error in updating database')


class FilmSearchView(ListView):
    model = Film

    def get(self, request, **kwargs):
        return render(request, 'film/search.html')

    def post(self, request):
        search_string = json.loads(request.body).get('searchText')
        films = Film.objects.filter(name__icontains=search_string)
        data = films.values()
        return JsonResponse(list(data), safe=False)


class FilmDetailView(DetailView):

    def get(self, request, **kwargs):
        """:return Film object, film's comments and comments form"""
        token = refresh_token_or_redirect(request)

        if not isinstance(token, str):
            return redirect('logout')

        context = ServiceFilmDetailView.execute({
            'pk': kwargs['pk'],
            'user': user_from_token(token),
        })
        return render(request, 'film/film_detail.html', context=context)

    def post(self, request, pk):
        """adds new comment to Film"""

        result_service = AddNewComment.execute({
            'pk': pk,
            'request': request,
        })
        if result_service['status']:
            return render(request, 'film/film_detail.html', context=result_service['context'])
        return HttpResponseNotFound('Error in creating comment')
