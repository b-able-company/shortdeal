"""
API URL routing for booth endpoints
"""
from django.urls import path
from .api_views import BoothDetailView, BoothContentsView

app_name = 'booths_api'

urlpatterns = [
    # Public booth profile
    path('<slug:slug>/', BoothDetailView.as_view(), name='booth_detail'),
    path('<slug:slug>/contents/', BoothContentsView.as_view(), name='booth_contents'),
]
