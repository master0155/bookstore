from django.urls import path, include
from rest_framework.routers import SimpleRouter
from tweet.viewsets import TweetViewSet

router = SimpleRouter()
router.register(r'tweets', TweetViewSet, basename='tweet')

urlpatterns = [
    path('', include(router.urls)),
]
