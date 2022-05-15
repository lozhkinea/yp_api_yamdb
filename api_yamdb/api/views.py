from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User

from api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    @action(methods=["get", "patch"], detail=True)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
