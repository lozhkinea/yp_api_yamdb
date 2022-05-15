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
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
# )
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet, basename='comments'
# )

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path(
        "auth/token/",
        TokenObtainPairView.as_view(),
        name="token",
    ),
]
