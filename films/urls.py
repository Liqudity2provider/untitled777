from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from .views import FilmSearchView, FilmDetailView, FilmsMainPage, UpdateFilmList

urlpatterns = [
    path('', FilmsMainPage.as_view(), name='index'),
    path('films/<str:params>/', FilmsMainPage.as_view(), name='index'),
    path('films/', FilmsMainPage.as_view(), name='index'),
    path('film/<int:pk>/', FilmDetailView.as_view(), name='film-detail'),
    path('update_db/', UpdateFilmList.as_view(), name='update-db'),
    path('search/', csrf_exempt(FilmSearchView.as_view()), name="search"),
]
