"""
URL routing for Settings endpoints
"""
from django.urls import path
from .settings_views import ProfileView, ChangePasswordView

app_name = 'settings_api'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
