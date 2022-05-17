from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api import views

app_name = "api"

router_v1 = SimpleRouter()
router_v1.register("users", views.UserViewSet, basename="users")
router_v1.register("titles", views.TitleViewSet, basename="titles")
router_v1.register("genres", views.GenreViewSet, basename="genres")
router_v1.register("categories", views.CategoryViewSet, basename="categories")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/signup/", views.signup, name="signup"),
    path("v1/auth/token/", views.token, name="token"),
]


# ???   ^[-a-zA-Z0-9_]+$
