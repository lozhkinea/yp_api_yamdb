from rest_framework import viewsets

from api.serializers import UserSerializer, ReviewSerializer, CommentSerializer
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
