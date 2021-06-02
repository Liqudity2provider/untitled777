from django.contrib.auth.models import User
from django.forms import model_to_dict
from rest_framework_simplejwt.backends import TokenBackend

from core.constants import jwt_service_object
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from django.http import HttpResponse


def user_from_token(token):
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user_id = valid_data['user_id']
        user = User.objects.get(pk=user_id)
        return user
    except:
        return None


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'token': str(refresh.access_token),
    }


def setcookie(request):

    refresh = request.data['refresh']
    token = request.data['token']

    response = HttpResponse("Cookie Set")
    response.set_cookie('refresh', refresh)
    response.set_cookie('token', token)

    return response


def getcookie(request):
    return HttpResponse(
        str(request.COOKIES))
