from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Post
import sys
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        return user

    def validate(self, data):
        validate_password(password=data.get('password'))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'posts']
