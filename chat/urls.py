# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='chat_entry'),
    path('<str:room_name>/', views.room, name='chat_room'),
]
