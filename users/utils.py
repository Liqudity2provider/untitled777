import time

import jwt
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.forms import model_to_dict
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from core.constants import jwt_service_object
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework_simplejwt.models import TokenUser

from users.forms import UserLoginForm


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
        str(request.COOKIES)
    )


def check_expiration(token, refresh):
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    if decoded_token.get('exp') > time.time():
        return None
    decoded_refresh = jwt.decode(refresh, options={"verify_signature": False})
    if decoded_refresh.get('exp') > time.time():
        refresh = RefreshToken(token=refresh)
        return {
            'refresh': str(refresh),
            'token': str(refresh.access_token),
        }
    return {
        'error': "Token has expired"
    }


def refresh_token_or_redirect(request):
    token = request.COOKIES.get('token')
    refresh = request.COOKIES.get('refresh')
    try:
        validation_result = check_expiration(token, refresh)

        if validation_result:
            token = validation_result.get('token')
            error = validation_result.get('error')
            if token:
                str(token)
            elif error:
                messages.error(request, 'Your token has been expired. Please login again.')
                return {
                    'error': 'token has been expired'
                }
        return token
    except:
        messages.error(request, 'Your token has been expired. Please login again.')
        return {
            'error': 'token has been expired'
        }
