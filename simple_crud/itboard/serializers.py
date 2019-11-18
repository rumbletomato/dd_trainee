from django.contrib.auth.models import User
from rest_framework import serializers

from itboard.models import Post, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'post', 'file')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    images = serializers.HyperlinkedRelatedField(read_only=True,
                                                 many=True,
                                                 required=False,
                                                 view_name='image-detail')

    class Meta:
        model = Post
        fields = ('id', 'created_ts', 'updated_ts', 'author', 'title', 'text', 'images')
