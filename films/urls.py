from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='index'),
    path('films/<str:params>/', views.index, name='index'),
    path('films/', views.index, name='index'),
    path('update_db/', views.update, name='update-db'),
    path('search/', csrf_exempt(views.search), name="search"),
]
