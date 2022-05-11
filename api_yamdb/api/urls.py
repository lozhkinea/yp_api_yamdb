from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from api import views

app_name = "api"

v1_router = routers.DefaultRouter()


urlpatterns = [
    path(
        "auth/token/",
        TokenObtainPairView.as_view(),
        name="token",
    ),
    path("", include(v1_router.urls)),
]
