from django.urls import path
from . import views

app_name = 'contents'

urlpatterns = [
    # Public URLs
    path('browse/', views.browse_view, name='browse'),
    path('<int:content_id>/', views.content_detail_view, name='detail'),

    # Studio URLs (Producer)
    path('studio/contents/', views.studio_content_list_view, name='studio_list'),
    path('studio/contents/new/', views.studio_content_create_view, name='studio_create'),
    path('studio/contents/<int:content_id>/edit/', views.studio_content_edit_view, name='studio_edit'),
]
