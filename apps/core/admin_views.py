"""
Admin dashboard API views
"""
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from apps.core.response import success_response, error_response
from apps.core.permissions import IsAdmin
from apps.accounts.models import User
from apps.contents.models import Content
from apps.offers.models import Offer
from apps.loi.models import LOI


@extend_schema(tags=['Admin'])
class AdminDashboardView(APIView):
    """Admin dashboard with summary statistics"""
    permission_classes = [IsAdmin]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='period',
                description='Period for stats (7d or 30d)',
                required=False,
                type=str,
                default='7d'
            )
        ],
        responses={
            200: OpenApiResponse(description='Dashboard data'),
            400: OpenApiResponse(description='Invalid period parameter')
        }
    )
    def get(self, request):
        """
        Get admin dashboard statistics (ADM-001~005)
        Query params: ?period=7d or ?period=30d
        """
        period = request.query_params.get('period', '7d')

        if period not in ['7d', '30d']:
            return error_response(
                message="Invalid period. Must be '7d' or '30d'",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Calculate period start date
        days = 7 if period == '7d' else 30
        period_start = timezone.now() - timedelta(days=days)

        # Summary statistics (all time)
        summary = {
            'total_users': User.objects.count(),
            'total_producers': User.objects.filter(role=User.Role.CREATOR).count(),
            'total_buyers': User.objects.filter(role=User.Role.BUYER).count(),
            'total_contents': Content.objects.exclude(status='deleted').count(),
            'total_offers': Offer.objects.count(),
            'pending_offers': Offer.objects.filter(status='pending').count(),
            'total_lois': LOI.objects.count(),
        }

        # Period statistics
        period_stats = {
            'period': period,
            'new_users': User.objects.filter(date_joined__gte=period_start).count(),
            'new_contents': Content.objects.filter(created_at__gte=period_start).count(),
            'new_offers': Offer.objects.filter(created_at__gte=period_start).count(),
            'new_lois': LOI.objects.filter(created_at__gte=period_start).count(),
        }

        # Recent users (last 10)
        recent_users = User.objects.order_by('-date_joined')[:10]
        recent_users_data = [
            {
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'company_name': user.company_name or user.username,
                'created_at': user.date_joined.isoformat(),
            }
            for user in recent_users
        ]

        # Recent contents (last 10)
        recent_contents = Content.objects.select_related('producer').order_by('-created_at')[:10]
        recent_contents_data = [
            {
                'id': content.id,
                'title': content.title,
                'producer': content.producer.company_name or content.producer.username,
                'status': content.status,
                'created_at': content.created_at.isoformat(),
            }
            for content in recent_contents
        ]

        # Recent offers (last 10)
        recent_offers = Offer.objects.select_related('buyer', 'content__producer').order_by('-created_at')[:10]
        recent_offers_data = [
            {
                'id': offer.id,
                'content_title': offer.content.title,
                'buyer': offer.buyer.company_name or offer.buyer.username,
                'producer': offer.content.producer.company_name or offer.content.producer.username,
                'status': offer.status,
                'offered_price': f"{offer.currency} {offer.offered_price:,.2f}",
                'created_at': offer.created_at.isoformat(),
            }
            for offer in recent_offers
        ]

        dashboard_data = {
            'summary': summary,
            'period_stats': period_stats,
            'recent_users': recent_users_data,
            'recent_contents': recent_contents_data,
            'recent_offers': recent_offers_data,
        }

        return success_response(
            data=dashboard_data,
            message="Dashboard data retrieved successfully"
        )
