from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    # Buyer URLs
    path('my/', views.buyer_offer_list_view, name='buyer_list'),
    path('my/<int:offer_id>/', views.buyer_offer_detail_view, name='buyer_detail'),
    path('create/<int:content_id>/', views.offer_create_view, name='create'),
]
