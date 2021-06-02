from django.shortcuts import render
from rest_framework.views import APIView
from core.constants import jwt_service_object
from users.utils import user_from_token


class IndexPage(APIView):

    def get(self, request):
        if request:
            user = user_from_token(request)
            return render(request, 'chat/index.html', context=user)
        return None


class EnterRoom(APIView):

    def get(self, request, room_name):
        return render(request, 'chat/room.html', {
            'room_name': room_name
        })
