import json
import requests
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from core import settings
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserLoginForm
from django.contrib import messages
from .serializers import UserSerializer
from .utils import user_from_token, get_tokens_for_user, refresh_token_or_redirect

path = settings.MY_URLS[settings.ACTIVE_URL]

headers = {
    'Content-Type': 'application/json',
}


class UserRegister(generics.CreateAPIView):
    """
    User Register View returning:
    - GET request - return HTML page with Form (Register Form)
    - POST request - retrieve User data, creates new User and return Login page
    """

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
                "form": UserRegisterForm(),
                "messages": [*output.get('errors')]
            })

        return Response(template_name='users/login.html', data={
            "form": UserRegisterForm(),
            "messages": output.get('errors')
        })


class UserProfile(APIView):
    """
    User Profile View returning:
    - GET request - return HTML page with Profile of User and
        User Update Form and Profile Update Form
    - POST request - retrieve data, updates User and user`s Profile

    Also checking that user in authenticated and token is valid or
        redirect to logout view
    """

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
        token = refresh_token_or_redirect(request)

        if not isinstance(token, str):
            return redirect('logout')

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


class LoginView(APIView):
    """
    User Login View returning:
    - GET request - return HTML page with User Login Form
    - POST request - retrieve data, authenticate User, create 'token' and 'refresh' and set them as cookie

    """

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        return Response(template_name='users/login.html', data={
            "form": UserLoginForm
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
                "form": UserLoginForm
            })


class LogoutView(APIView):
    """
    User Logout View returning:
    - GET request - delete cookie and return Logout HTML page   

    """

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        response = Response(template_name='users/logout.html', data={
            'user': None
        })
        response.delete_cookie('refresh')
        response.delete_cookie('token')

        return response
