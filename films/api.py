from rest_framework import generics

from films.models import Film, Comment
from films.serializers import FilmSerializer, CommentSerializer


class FilmApiDetailView(generics.RetrieveUpdateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


class FilmApiListView(generics.ListCreateAPIView):
    """
        List all posts, or create a new.
        """
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    model = Film


class CommentApiDetailView(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentApiListView(generics.ListCreateAPIView):
    """
        List all comments, or create a new.
        """
    queryset = Comment.objects.filter(deleted=False)
    serializer_class = CommentSerializer
