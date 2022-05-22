from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins
from rest_framework import permissions as rest_permissions
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from reviews.models import Category, Genre, Review, Title
from users.models import User

from api import filter, permissions, serializers


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAdminOrAuthenticated,)
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.order_by('id')

    @action(methods=['get', 'patch'], detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        if request.GET:
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        if (
            self.request.user.role in ['user']
            and 'role' in serializer.validated_data
        ):
            serializer.validated_data.pop('role')
        serializer.save()


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TitleListSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filter.TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TitleListSerializer
        else:
            return serializers.TitleSerializer

    def get_queryset(self):
        return Title.objects.order_by('id')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_data = serializer.save()
        create_serializer = serializers.TitleListSerializer(create_data)
        return Response(create_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        updated_serializer = serializers.TitleListSerializer(updated_instance)
        return Response(updated_serializer.data)


class CreateListDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(CreateListDeleteViewSet):
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.order_by('name')


class GenreViewSet(CreateListDeleteViewSet):
    serializer_class = serializers.GenreSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_queryset(self):
        return Genre.objects.order_by('name')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (
        rest_permissions.IsAuthenticatedOrReadOnly,
        permissions.ReviewAndComment,
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
    serializer_class = serializers.CommentSerializer
    permission_classes = (
        rest_permissions.IsAuthenticatedOrReadOnly,
        permissions.ReviewAndComment,
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


class UserSignupView(CreateAPIView):
    model = User
    permission_classes = [rest_permissions.AllowAny]
    serializer_class = serializers.UserSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )


class UserTokenView(CreateAPIView):
    model = User
    permission_classes = [rest_permissions.AllowAny]
    serializer_class = serializers.UserTokenSerializer
