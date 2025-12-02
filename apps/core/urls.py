"""
URL routing for Core template views
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('admin/', views.admin_dashboard_view, name='admin_dashboard'),
]
