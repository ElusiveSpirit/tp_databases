from django.shortcuts import get_object_or_404
from rest_framework import serializers

from user.serializers import UserSerializer
from user.models import User

from .models import Forum, Post, Thread


class ForumSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Forum
        fields = ('id', 'name', 'short_name', 'user')
        read_only_fields = ['id']

    def save(self):
        self.validated_data['user'] = get_object_or_404(User, email=self.validated_data.get('user'))
        return super(ForumSerializer, self).save()


class ForumDetailSerializer(serializers.ModelSerializer):
    RELATED_USER = ('id', 'name', 'short_name', 'user')

    def __init__(self, *args, **kwargs):
        if 'related' in kwargs and 'user' in kwargs.get('related'):
            self.Meta.fields = self.RELATED_USER
            self.fields['user'] = UserSerializer()
            del kwargs['related']

        return super(ForumDetailSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Forum
        fields = ('id', 'name', 'short_name')


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
