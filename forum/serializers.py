from rest_framework import serializers

from user.serializers import UserSerializer

from .models import Forum, Post, Thread


class ForumSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Forum
        fields = ('id', 'name', 'short_name', 'user')


class ForumDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Forum
        fields = ('id', 'name', 'short_name', 'user')


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    forum = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ('id', 'date', 'forum', 'isApproved', 'isDeleted', 'isEdited', 'isHighlighted',
                  'isSpam', 'message', 'parent', 'thread', 'user')


class ThreadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    forum = serializers.StringRelatedField()

    class Meta:
        model = Thread
        fields = ('id', 'date', 'forum', 'isClosed', 'isDeleted',
                  'message', 'slug', 'title', 'user')
