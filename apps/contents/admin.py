"""
Admin configuration for Content model
"""
from django.contrib import admin
from .models import Content


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'producer', 'status', 'price', 'currency', 'view_count', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('title', 'description', 'producer__username', 'producer__company_name')
    readonly_fields = ('view_count', 'created_at', 'updated_at', 'deleted_at')
    list_per_page = 50

    fieldsets = (
        ('Basic Information', {
            'fields': ('producer', 'title', 'description', 'thumbnail')
        }),
        ('Content Details', {
            'fields': ('genre_tags', 'duration_seconds', 'video_url')
        }),
        ('Pricing', {
            'fields': ('price', 'currency')
        }),
        ('Status & Visibility', {
            'fields': ('status',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at', 'deleted_at')
        }),
    )

    def get_queryset(self, request):
        """Include soft-deleted items in admin"""
        return Content.objects.all()
