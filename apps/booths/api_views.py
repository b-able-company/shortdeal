"""
API views for public booth profiles
"""
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db.models import F
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.core.response import success_response, error_response, paginated_response
from apps.core.constants import CONTENT_STATUS_PUBLIC
from apps.contents.serializers import ContentPublicSerializer
from .models import Booth
from .serializers import BoothPublicSerializer


@extend_schema(tags=['Booth - Public'])
class BoothDetailView(APIView):
    """Public booth profile view"""
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            200: BoothPublicSerializer,
            404: OpenApiResponse(description='Booth not found')
        }
    )
    def get(self, request, slug):
        """Get booth profile by slug"""
        try:
            booth = Booth.objects.select_related('producer').get(slug=slug)
        except Booth.DoesNotExist:
            return error_response(
                message="Booth not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Increment view count (atomic)
        Booth.objects.filter(pk=booth.pk).update(view_count=F('view_count') + 1)
        booth.refresh_from_db(fields=['view_count'])

        serializer = BoothPublicSerializer(booth)
        return success_response(
            data=serializer.data,
            message="Booth profile retrieved successfully"
        )


@extend_schema(tags=['Booth - Public'])
class BoothContentsView(APIView):
    """List all public contents from a booth"""
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            200: ContentPublicSerializer(many=True),
            404: OpenApiResponse(description='Booth not found')
        }
    )
    def get(self, request, slug):
        """Get all public contents from booth"""
        try:
            booth = Booth.objects.select_related('producer').get(slug=slug)
        except Booth.DoesNotExist:
            return error_response(
                message="Booth not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Get public contents from this producer
        queryset = booth.producer.contents.filter(
            status=CONTENT_STATUS_PUBLIC
        ).order_by('-created_at')

        return paginated_response(
            queryset,
            ContentPublicSerializer,
            request,
            message=f"Contents from {booth.slug} retrieved successfully"
        )
