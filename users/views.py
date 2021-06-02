import json

import requests
import rest_framework_simplejwt
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core import serializers
from django.forms.models import model_to_dict
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.views import token_obtain_pair
from django.shortcuts import render, redirect
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.generic.detail import BaseDetailView
from rest_framework import generics, permissions
from django.contrib.auth import authenticate, login

from blog.models import Post
from blog.serializers import PostSerializer
from core.constants import jwt_service_object
from django.views.generic import TemplateView
from django.contrib.auth import logout, get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_social_auth.serializers import UserSerializer
from rest_social_auth.views import KnoxAuthMixin, SimpleJWTAuthMixin
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile
from .serializers import UserSerializer
from .utils import user_from_token, get_tokens_for_user

path = 'http://127.0.0.1:8000/'
headers = {
    'Content-Type': 'application/json',
}


class UserRegister(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response(template_name='users/register.html', data={
            "form": UserRegisterForm,
        })

    def post(self, request, *args, **kwargs):
        form_data = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "password": request.data.get("password1"),
            "password2": request.data.get("password2")
        }
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(
            path + 'api/users/',
            headers=headers,
            data=json.dumps(form_data)
        )

        output = response.json()
        if output.get("errors"):
            return Response(template_name='users/register.html', data={
                "form": UserRegisterForm,
                "messages": [*output.get('errors')]
            })

        return Response(template_name='users/login.html', data={
            "form": UserRegisterForm,
            "messages": output.get('errors')
        })


class UserProfile(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('token')
        user = user_from_token(token)
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Account has been updated')
            return redirect('profile')

    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get('token')
        if token:  # if user is authenticated
            user = user_from_token(token=token)

            u_form = UserUpdateForm(instance=user)
            p_form = ProfileUpdateForm(instance=user)
            context = {
                "user": {
                    "image": user.profile.image
                },
                'u_form': u_form,
                'p_form': p_form,
            }

            return render(request, 'users/profile.html', context)
        else:
            print('User is not authenticated')
            return render(request, 'users/login.html')


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    form_class = UserLoginForm

    def get(self, request, *args, **kwargs):
        return Response(template_name='users/login.html', data={
            "form": self.form_class
        })

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            pair_tokens = get_tokens_for_user(user)  # creating tokens for user authentication
            response = requests.get(
                path + 'api/posts/',
                headers=headers,
                data=json.dumps({}),
            )
            result = Response(
                template_name='blog/home.html',
                headers=headers,
                data={
                    "posts": response.json(),
                }
            )
            result.set_cookie("refresh", pair_tokens["refresh"])
            result.set_cookie("token", pair_tokens["token"])
            return result

        else:
            messages.error(request, "Cannot find user with this email and password")
            return Response(template_name='users/login.html', data={
                "form": self.form_class
            })


class LogoutView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        response = Response(template_name='users/logout.html', data={
            'user': None
        })
        response.delete_cookie('refresh')
        response.delete_cookie('token')

        return response
