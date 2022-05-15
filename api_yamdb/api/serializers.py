from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class TokenSerializer(serializers.Serializer):
    class Meta:
        fields = (
            "username",
            "confirmation_code",
        )
