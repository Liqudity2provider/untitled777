from rest_framework import serializers
from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_image = serializers.ReadOnlyField(source='author.profile.image')

    class Meta:
        model = Post
        fields = "__all__"
