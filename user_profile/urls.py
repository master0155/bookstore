from django.urls import path, include
from rest_framework.routers import SimpleRouter
from user_profile.viewsets import UserProfileViewSet, UserViewSet

router = SimpleRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
