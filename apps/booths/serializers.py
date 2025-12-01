"""
Serializers for Booth model
"""
from rest_framework import serializers
from .models import Booth


class BoothPublicSerializer(serializers.ModelSerializer):
    """Public serializer for booth profile"""

    producer_name = serializers.CharField(source='producer.company_name', read_only=True)
    producer_username = serializers.CharField(source='producer.username', read_only=True)
    producer_logo = serializers.ImageField(source='producer.logo', read_only=True)
    producer_country = serializers.CharField(source='producer.country', read_only=True)
    producer_genre_tags = serializers.ListField(source='producer.genre_tags', read_only=True)
    content_count = serializers.SerializerMethodField()

    class Meta:
        model = Booth
        fields = (
            'slug', 'view_count', 'is_boosted', 'created_at',
            'producer_name', 'producer_username', 'producer_logo',
            'producer_country', 'producer_genre_tags', 'content_count'
        )
        read_only_fields = fields

    def get_content_count(self, obj):
        """Get count of public contents"""
        return obj.producer.contents.filter(status='public').count()
