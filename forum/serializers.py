from rest_framework import serializers

from user.serializers import UserSerializer

from .models import Forum, Post


class ForumSerializer(serializers.ModelSerializer):
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
