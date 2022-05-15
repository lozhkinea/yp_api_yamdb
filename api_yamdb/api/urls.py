from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from api import views

app_name = "api"

router_v1 = SimpleRouter()
router_v1.register("users", views.UserViewSet, basename="users")
# router_v1.register("titles", views.TitleViewSet, basename="titles")
# router_v1.register("genres", views.GenreViewSet, basename="genres")
# router_v1.register("categories", views.CategoryViewSet, basename="categories")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path(
        "v1/auth/signup/",
        views.UserViewSet.as_view({"post": "create"}, name="signup"),
    ),
    path(
        "v1/auth/token/",
        TokenObtainPairView.as_view(),
        name="token",
    ),
]
