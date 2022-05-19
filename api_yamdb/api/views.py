from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Review, Title
from users.models import User

from api import serializers
from api.permissions import IsAdminOrAuthenticated, ReviewAndComment
from api.serializers import CommentSerializer, ReviewSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAdminOrAuthenticated,)
    pagination_class = PageNumberPagination
    queryset = User.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ReviewAndComment,
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ReviewAndComment,
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)

    @action(methods=['get', 'patch'], detail=True)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def signup(request):
    '''
    Регистрация нового пользователя {username}.
    Отправка кода подтверждения на {email}.
    '''
    serializer = serializers.UserSignupSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    code = default_token_generator.make_token(user)
    serializer.update(user, {'confirmation_code': code})
    subject = 'Код подтверждения регистрации на YaMDb'
    message = f'Привет {user}, твой код подтверждения: {code}'
    EmailMessage(subject, message, to=[user.email]).send()
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token(request):
    '''
    Пользователь отправляет POST-запрос с параметрами
    {username} и {confirmation_code} на эндпоинт /api/v1/auth/token/,
    в ответе на запрос ему приходит token (JWT-токен).
    '''
    serializer = serializers.UserTokenSerializer(data=request.data)
    if serializer.is_valid():
        return Response(
            {'username': 'A user with that username not exists'},
            status=status.HTTP_404_NOT_FOUND,
        )
    if 'username' not in serializer.data:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=serializer.data['username']).exists():
        code = serializer.data['confirmation_code']
        user = User.objects.get(username=serializer.data['username'])
        msg = f'Сonfirmation code {code} is invalid [{user.confirmation_code}]'
        if user.confirmation_code != code:
            return Response(
                {
                    'confirmation_code': msg,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    refresh = RefreshToken.for_user(user)
    return Response(
        {'token': str(refresh.access_token)}, status=status.HTTP_200_OK
    )
