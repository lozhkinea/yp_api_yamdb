from api import views
from django.urls import include, path
from rest_framework.routers import SimpleRouter


app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register('users', views.UserViewSet, basename='users')
router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register('genres', views.GenreViewSet, basename='genres')
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', views.UserSignupView.as_view(), name='signup'),
    path('v1/auth/token/', views.UserTokenView.as_view(), name='token'),
]
