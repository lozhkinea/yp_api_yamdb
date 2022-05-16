from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets, mixins
# from rest_framework.pagination import LimitOffsetPagination

from .serializers import UserSerializer, TitleSerializer, CategorySerializer, GenreSerializer
from .permissions import IsAdminOrReadOnly
from users.models import User
from reviews.models import Title, Category, Genre


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    # выборка объектов модели
    queryset = Title.objects.all()
    # какой сериализатор будет применён для валидации и сериализации
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    # Фильтровать будем по следующим полям
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    # def perform_create(self, serializer):
    #     genre
    #     category


class CreateListDeleteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)