from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import update_session_auth_hash
from .models import User
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    ChangePasswordSerializer
)


class UserRegistrationAPIView(generics.CreateAPIView):
    """API endpoint for user registration"""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """API endpoint for viewing and updating user profile"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """API endpoint for changing password"""
    serializer = ChangePasswordSerializer(data=request.data)
    
    if serializer.is_valid():
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"old_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        update_session_auth_hash(request, user)
        
        return Response(
            {"message": "Password updated successfully."},
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    """API endpoint for user statistics"""
    user = request.user
    
    # Import here to avoid circular imports
    from core.models import ImageRecord
    
    total_uploads = ImageRecord.objects.filter(user=user).count()
    analyzed_images = ImageRecord.objects.filter(user=user, status='analyzed').count()
    pending_images = ImageRecord.objects.filter(user=user, status='pending').count()
    
    return Response({
        'total_uploads': total_uploads,
        'analyzed_images': analyzed_images,
        'pending_images': pending_images,
        'user_role': user.role,
        'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
    })
