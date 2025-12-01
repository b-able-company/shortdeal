"""
URL routing for Admin endpoints
"""
from django.urls import path
from .admin_views import AdminDashboardView

app_name = 'admin_api'

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='dashboard'),
]
