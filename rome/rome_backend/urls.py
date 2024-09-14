from django.urls import path, include

from . import views
from rome_backend.views import get_assets


urlpatterns = [
    path('get-assets/', get_assets, name='get-assets'),
    # path('api/', include('rome_backend.urls')),
    # path('', views.index, name = 'index')
    # path("", views.index, name="index"),
]