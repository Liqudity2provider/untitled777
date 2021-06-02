# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='chat_entry'),
    path('<str:room_name>/', views.EnterRoom.as_view(), name='chat_room'),
]
