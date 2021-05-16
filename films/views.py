import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from films import utils_parse
from films.models import Film, Genre


def index(request, params=''):
    if len(params) > 2:
        contex = {
            'data_films': Film.objects.filter(genres__name=params),
            'genres': Genre.objects.all(),
        }
    else:
        contex = {
            'data_films': Film.objects.all(),
            'genres': Genre.objects.all(),
        }
    return render(request, 'film/index.html', contex)


def update(request):
    to_delete = Genre.objects.all()
    to_delete.delete()
    to_delete = Film.objects.all()
    to_delete.delete()

    list_genres = utils_parse.return_genres()
    for genre in list_genres:
        new_genre = Genre(name=genre)
        new_genre.save()

    list_with_films = utils_parse.parse_func()

    for film in list_with_films:
        try:
            new_film = Film(name=film['name'], link=film['link'], image=film['image'],
                            rating=film['rating'], )
            new_film.save()

            for genre in film['genres']:
                genre = Genre.objects.filter(name__contains=genre).first()
                new_film.genres.add(genre)
                new_film.save()
        except:
            print('Error adding film to db')

    return render(request, 'film/done.html', {})


def search(request):
    if request.method == "POST":
        search_string = json.loads(request.body).get('searchText')

        films = Film.objects.filter(name__icontains=search_string)
        data = films.values()
        return JsonResponse(list(data), safe=False)
    return render(request, 'film/search.html')