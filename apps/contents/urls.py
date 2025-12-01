from django.urls import path
from . import views

app_name = 'contents'

urlpatterns = [
    path('browse/', views.browse_view, name='browse'),
    path('<int:content_id>/', views.content_detail_view, name='detail'),
]
