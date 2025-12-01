"""
API URL routing for content endpoints
"""
from django.urls import path
from .api_views import ContentListView, ContentDetailView

app_name = 'contents_api'

urlpatterns = [
    # Public content browsing
    path('', ContentListView.as_view(), name='content_list'),
    path('<int:pk>/', ContentDetailView.as_view(), name='content_detail'),
]
