from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AccountViewSet, LoginView, UserViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]
