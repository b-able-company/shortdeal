"""
Admin configuration for LOI model
"""
from django.contrib import admin
from .models import LOI


@admin.register(LOI)
class LOIAdmin(admin.ModelAdmin):
    list_display = ('document_number', 'buyer_company', 'producer_company', 'agreed_price', 'currency', 'is_pdf_ready', 'created_at')
    list_filter = ('currency', 'created_at', 'pdf_generated_at')
    search_fields = ('document_number', 'content_title', 'buyer_company', 'producer_company')
    readonly_fields = ('document_number', 'created_at', 'updated_at', 'pdf_generated_at')
    list_per_page = 50

    fieldsets = (
        ('Document Info', {
            'fields': ('document_number', 'offer')
        }),
        ('Parties', {
            'fields': ('buyer', 'buyer_company', 'buyer_country', 'producer', 'producer_company', 'producer_country')
        }),
        ('Content & Deal', {
            'fields': ('content_title', 'content_description', 'agreed_price', 'currency')
        }),
        ('PDF', {
            'fields': ('pdf_file', 'pdf_generated_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_queryset(self, request):
        """Optimize queries"""
        return super().get_queryset(request).select_related('buyer', 'producer', 'offer')
