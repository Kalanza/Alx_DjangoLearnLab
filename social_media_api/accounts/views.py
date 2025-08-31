from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer

class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    API view for user login.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating user profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

# Follow and unfollow endpoints
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        """
        Authenticated user follows another user.
        """
        to_follow = get_object_or_404(CustomUser, id=user_id)
        if to_follow == request.user:
            return Response({'detail': 'You cannot follow yourself.'}, status=400)
        if request.user.following.filter(id=to_follow.id).exists():
            return Response({'detail': 'Already following this user.'}, status=400)
        request.user.following.add(to_follow)
        return Response({'detail': f'You are now following {to_follow.username}.'}, status=200)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        """
        Authenticated user unfollows another user.
        """
        to_unfollow = get_object_or_404(CustomUser, id=user_id)
        if to_unfollow == request.user:
            return Response({'detail': 'You cannot unfollow yourself.'}, status=400)
        if not request.user.following.filter(id=to_unfollow.id).exists():
            return Response({'detail': 'You are not following this user.'}, status=400)
        request.user.following.remove(to_unfollow)
        return Response({'detail': f'You have unfollowed {to_unfollow.username}.'}, status=200)
