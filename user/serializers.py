from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'about', 'isAnonymous')


class UserDetailSerializer(serializers.ModelSerializer):
    following = serializers.StringRelatedField(many=True)
    followers = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'about', 'isAnonymous',
                  'following', 'followers')


class UserFollowSerializer(serializers.Serializer):
    follower = serializers.EmailField()
    followee = serializers.EmailField()

    def save(self):
        follower = get_object_or_404(User, email=self.validated_data.get('follower'))
        followee = get_object_or_404(User, email=self.validated_data.get('followee'))

        follower.following.add(followee)

        return follower
