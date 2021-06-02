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

    def get(self, request, *args, **kwargs):
        data = list(Post.objects.values())
        user_queryset = User.objects.all()
        [post.update({
            "author_image": user_queryset.get(pk=post.get('author_id')).profile.image,
            "author": user_queryset.get(pk=post.get('author_id')).username,
        }) for post in data]
        return JsonResponse(data, safe=False)


class PostApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post instance.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs.get("pk"))
        response = self.retrieve(request, *args, **kwargs)
        user_queryset = User.objects.all()
        response.data.update({"author_image": user_queryset.get(pk=post.author_id).profile.image})
        return JsonResponse(response.data, safe=False)
