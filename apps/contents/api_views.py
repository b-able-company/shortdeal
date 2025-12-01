"""
API views for public content browsing
"""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from apps.core.response import success_response, error_response, paginated_response
from apps.core.constants import CONTENT_STATUS_PUBLIC
from .models import Content
from .serializers import ContentPublicSerializer, ContentDetailSerializer


@extend_schema(tags=['Content - Public'])
class ContentListView(generics.ListAPIView):
    """Public content listing with filters and search"""
    permission_classes = [AllowAny]
    serializer_class = ContentPublicSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter('search', str, description='Search in title and description'),
            OpenApiParameter('genre', str, description='Filter by genre tag'),
            OpenApiParameter('min_price', float, description='Minimum price'),
            OpenApiParameter('max_price', float, description='Maximum price'),
            OpenApiParameter('currency', str, description='Currency code (USD, KRW, etc)'),
            OpenApiParameter('ordering', str, description='Sort by: -created_at, price, -price, view_count'),
        ],
        responses={200: ContentPublicSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        """List all public contents with filtering and sorting"""
        queryset = self.get_queryset()

        # Search
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # Genre filter
        genre = request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre_tags__contains=[genre])

        # Price range filter
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        if min_price is not None and max_price is not None:
            try:
                min_price = float(min_price)
                max_price = float(max_price)
                if min_price > max_price:
                    return error_response(
                        message="min_price cannot be greater than max_price",
                        status_code=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return error_response(
                    message="Invalid price range values",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        # Currency filter
        currency = request.query_params.get('currency')
        if currency:
            queryset = queryset.filter(currency=currency.upper())

        # Ordering
        ordering = request.query_params.get('ordering', '-created_at')
        allowed_orderings = ['-created_at', 'created_at', 'price', '-price', 'view_count', '-view_count']
        if ordering in allowed_orderings:
            queryset = queryset.order_by(ordering)

        return paginated_response(
            queryset,
            ContentPublicSerializer,
            request,
            message="Contents retrieved successfully"
        )

    def get_queryset(self):
        """Only return public, non-deleted contents"""
        return Content.objects.filter(status=CONTENT_STATUS_PUBLIC).select_related('producer')


@extend_schema(tags=['Content - Public'])
class ContentDetailView(APIView):
    """Public content detail view"""
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            200: ContentDetailSerializer,
            404: OpenApiResponse(description='Content not found')
        }
    )
    def get(self, request, pk):
        """Get content detail and increment view count"""
        try:
            content = Content.objects.select_related('producer').get(
                pk=pk,
                status=CONTENT_STATUS_PUBLIC
            )
        except Content.DoesNotExist:
            return error_response(
                message="Content not found or not available",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Increment view count (atomic)
        content.increment_view_count()

        serializer = ContentDetailSerializer(content)
        return success_response(
            data=serializer.data,
            message="Content retrieved successfully"
        )
