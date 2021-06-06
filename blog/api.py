import json

from django.contrib.auth.models import User
from django.core import serializers
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.response import Response

from blog.models import Post
from blog.permissions import IsOwnerOrReadOnly
from blog.serializers import PostSerializer


class PostApiListView(generics.ListCreateAPIView):
    """
        List all posts, or create a new.
        """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post instance.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
