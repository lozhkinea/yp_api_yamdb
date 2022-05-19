from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title
from users.models import User
from api import filter, serializers
from .permissions import IsAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'

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
        {'token': str(refresh.access_token)},
        status=status.HTTP_200_OK
    )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleListSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = filter.TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TitleListSerializer
        else:
            return serializers.TitleSerializer


class CreateListDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(CreateListDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
