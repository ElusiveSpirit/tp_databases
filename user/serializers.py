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


class UserUpdateSerializer(serializers.Serializer):
    user = serializers.EmailField()
    about = serializers.CharField()
    name = serializers.CharField(max_length=40)

    def save(self):
        user = get_object_or_404(User, email=self.validated_data.get('user'))
        user.about = self.validated_data.get('about')
        user.name = self.validated_data.get('name')
        user.save()
        return user


class UserFollowSerializer(serializers.Serializer):
    follower = serializers.EmailField()
    followee = serializers.EmailField()

    def save(self):
        follower = get_object_or_404(User, email=self.validated_data.get('follower'))
        followee = get_object_or_404(User, email=self.validated_data.get('followee'))

        follower.following.add(followee)

        return follower

    def remove(self):
        follower = get_object_or_404(User, email=self.validated_data.get('follower'))
        followee = get_object_or_404(User, email=self.validated_data.get('followee'))

        follower.following.remove(followee)

        return follower
