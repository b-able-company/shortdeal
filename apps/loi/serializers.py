"""
Serializers for LOI model
"""
from rest_framework import serializers
from .models import LOI


class LOISerializer(serializers.ModelSerializer):
    """Serializer for LOI documents"""

    offer_id = serializers.IntegerField(source='offer.id', read_only=True)
    is_pdf_ready = serializers.BooleanField(read_only=True)

    class Meta:
        model = LOI
        fields = (
            'id', 'document_number', 'offer_id',
            'buyer', 'buyer_company', 'buyer_country',
            'producer', 'producer_company', 'producer_country',
            'content_title', 'content_description',
            'agreed_price', 'currency',
            'pdf_file', 'pdf_generated_at', 'is_pdf_ready',
            'created_at', 'updated_at'
        )
        read_only_fields = fields
