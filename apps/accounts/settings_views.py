"""
API views for Settings/Profile management
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.core.response import success_response, error_response
from .settings_serializers import ProfileSerializer, ChangePasswordSerializer


@extend_schema(tags=['Settings'])
class ProfileView(APIView):
    """Get and update user profile"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: ProfileSerializer}
    )
    def get(self, request):
        """Get current user profile (SET-001)"""
        serializer = ProfileSerializer(request.user, context={'request': request})
        return success_response(
            data=serializer.data,
            message="Profile retrieved successfully"
        )

    @extend_schema(
        request=ProfileSerializer,
        responses={200: ProfileSerializer}
    )
    def patch(self, request):
        """Update current user profile (SET-001)"""
        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return success_response(
                data=serializer.data,
                message="Profile updated successfully"
            )

        return error_response(
            message="Profile update failed",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(tags=['Settings'])
class ChangePasswordView(APIView):
    """Change user password"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description='Password changed successfully'),
            400: OpenApiResponse(description='Validation error')
        }
    )
    def post(self, request):
        """Change user password (SET-002)"""
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return success_response(
                message="Password changed successfully"
            )

        return error_response(
            message="Password change failed",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
