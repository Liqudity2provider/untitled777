from collections import OrderedDict
from datetime import datetime
from multiprocessing import Pool

from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject

from films.models import Film, Comment, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)


class FilmSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField()
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Film
        fields = ['id', 'name', 'link', 'image_url', 'rating', 'genres', 'comments']


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
