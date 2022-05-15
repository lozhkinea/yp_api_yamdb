from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
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
    subject = "Код подтверждения регистрации на YaMDb"
    message = f"Привет {user}, твой код подтверждения: {code}"
    EmailMessage(subject, message, to=[user.email]).send()
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def authtoken(request):
    """
    Пользователь отправляет POST-запрос с параметрами
    {username} и {confirmation_code} на эндпоинт /api/v1/auth/token/,
    в ответе на запрос ему приходит token (JWT-токен).
    """
    serializer = serializers.TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = serializer.instance
    refresh = RefreshToken.for_user(user)
    return Response(
        {"token": str(refresh.access_token)}, status=status.HTTP_200_OK
    )
