import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from blog.models import Post
from blog.permissions import IsOwnerOrReadOnly
from blog.serializers import PostSerializer
from users.models import Profile
from users.serializers import UserSerializer, ProfileSerializer


class UserApiListView(generics.ListCreateAPIView):
    """
        List all posts, or create a new.
        """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    model = User

    def create(self, request, *args, **kwargs):
        print(request.data)
        data_to_create = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "password": request.data.get("password"),
            "password2": request.data.get("password2")
        }
        serializer = self.get_serializer(data=data_to_create)
        headers = self.headers
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print('api view exception')
            return Response(data={
                "errors": e.args
            }, headers=headers)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class UserApiDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a post instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileApiDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileApiListView(generics.ListCreateAPIView):
    """
        List all posts, or create a new.
        """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    model = Profile
