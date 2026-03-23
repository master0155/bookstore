from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer, UserSerializer


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Retorna o perfil do usuário autenticado"""
        profile = request.user.profile
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Atualiza o perfil do usuário autenticado"""
        profile = request.user.profile
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """Segue um usuário"""
        user_to_follow = self.get_object().user
        request.user.profile.following.add(user_to_follow)
        return Response({'status': f'Agora seguindo {user_to_follow.username}'})
    
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """Para de seguir um usuário"""
        user_to_unfollow = self.get_object().user
        request.user.profile.following.remove(user_to_unfollow)
        return Response({'status': f'Deixou de seguir {user_to_unfollow.username}'})


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
