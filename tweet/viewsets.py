from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from tweet.models import Tweet, Like, Comment
from tweet.serializers import TweetSerializer, CommentSerializer, LikeSerializer


class TweetViewSet(ModelViewSet):
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

    def get_queryset(self):
        return Tweet.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def feed(self, request):
        """Retorna tweets apenas das pessoas que o usuário segue"""
        following_users = request.user.profile.following.all()
        tweets = Tweet.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = self.get_serializer(tweets, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        tweet = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
        if not created:
            return Response({'detail': 'Você já curtiu este tweet.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Tweet curtido!'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        tweet = self.get_object()
        deleted, _ = Like.objects.filter(user=request.user, tweet=tweet).delete()
        if not deleted:
            return Response({'detail': 'Você não curtiu este tweet.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Curtida removida!'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def comment(self, request, pk=None):
        tweet = self.get_object()
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, tweet=tweet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        tweet = self.get_object()
        comments = tweet.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
