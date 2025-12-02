from django.urls import path
from . import views

app_name = 'loi'

urlpatterns = [
    # LOI list and detail
    path('', views.loi_list_view, name='list'),
    path('<int:loi_id>/', views.loi_detail_view, name='detail'),
]
