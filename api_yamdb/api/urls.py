from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from api import views

app_name = "api"

router_v1 = SimpleRouter()
router_v1.register("titles", TitleViewSet, basename="titles")
router_v1.register("genres", GenreViewSet, basename="genres")
router_v1.register("categories", CategoryViewSet, basename="categories")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path(
        "auth/token/",
        TokenObtainPairView.as_view(),
        name="token",
    ),
]
