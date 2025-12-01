from django.urls import path
from apps.contents.views import booth_view

app_name = 'booths'

urlpatterns = [
    path('<slug:slug>/', booth_view, name='detail'),
]
