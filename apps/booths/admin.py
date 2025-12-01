"""
Admin configuration for Booth model
"""
from django.contrib import admin
from .models import Booth


@admin.register(Booth)
class BoothAdmin(admin.ModelAdmin):
    list_display = ('slug', 'producer', 'view_count', 'is_boosted', 'created_at')
    list_filter = ('is_boosted', 'created_at')
    search_fields = ('slug', 'producer__username', 'producer__company_name')
    readonly_fields = ('created_at', 'updated_at', 'view_count')
    fieldsets = (
        ('Basic Info', {
            'fields': ('producer', 'slug')
        }),
        ('Boost Settings', {
            'fields': ('is_boosted', 'boost_expires_at')
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at')
        }),
    )
