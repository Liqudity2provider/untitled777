from rest_framework import serializers

from films.models import Film, Comment


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'name', 'image', 'link', 'rating', 'genres', 'comments']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'film',
            'author',
            'parent',
            'content',
            'publish',
            'status',
        ]
