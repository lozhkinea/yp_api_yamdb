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


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError('Cannot create user "me"')
        return data


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "confirmation_code",
        )
