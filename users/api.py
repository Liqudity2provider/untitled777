import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework_swagger import renderers

from blog.models import Post
from blog.permissions import IsOwnerOrReadOnly
from blog.serializers import PostSerializer
from users.models import Profile
from users.serializers import UserSerializer, ProfileSerializer


class UserApiListView(generics.ListCreateAPIView):
    """
        List all users, or create a new.
        """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    model = User


class UserApiDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a user instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileApiDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileApiListView(generics.ListCreateAPIView):
    """
        List all profiles, or create a new.
        """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    model = Profile
