from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'about', 'isAnonymous')

    def is_exists(self):
        print(self.validated_data)
        try:
            User.objects.get(email=self.validated_data['email'])
        except User.DoesNotExist:
            return False
        return True
