from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

from api import serializers


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    @action(methods=["get", "patch"], detail=True)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def signup(request):
    """
    Регистрация нового пользователя {username}.
    Отправка кода подтверждения на {email}.
    """
    serializer = serializers.UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    code = default_token_generator.make_token(user)
    serializer.update(user, {"confirmation_code": code})
    subject = "Код подтверждения регистрации на YaMDb"
    message = f"Привет {user}, твой код подтверждения: {code}"
    EmailMessage(subject, message, to=[user.email]).send()
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def token(request):
    """
    Пользователь отправляет POST-запрос с параметрами
    {username} и {confirmation_code} на эндпоинт /api/v1/auth/token/,
    в ответе на запрос ему приходит token (JWT-токен).
    """
    serializer = serializers.TokenSerializer(data=request.data)
    if serializer.is_valid():
        return Response(
            {"username": "A user with that username not exists"},
            status=status.HTTP_404_NOT_FOUND,
        )
    user = get_object_or_404(User, username=serializer.data["username"])
    code = serializer.data["confirmation_code"]
    if user.confirmation_code != code:
        return Response(
            {
                "confirmation_code": f"Сonfirmation code {code} is invalid [{user.confirmation_code}]"
            },
            status=status.HTTP_404_NOT_FOUND,
        )
    refresh = RefreshToken.for_user(user)
    return Response(
        {"token": str(refresh.access_token)}, status=status.HTTP_200_OK
    )
