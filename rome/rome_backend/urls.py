from django.urls import path

from . import views
from rome_backend.views import get_assets


urlpatterns = [
    path('api/get-assets/', get_assets, name='get-assets'),
    path("", views.index, name="index"),
]