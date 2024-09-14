from django.urls import path, include

from . import views
from rome_backend.views import get_assets, get_zip

urlpatterns = [
    path('get-assets/', get_assets, name='get-assets'),
    path("get-zip/", get_zip, name="get-zip")
    # path('api/', include('rome_backend.urls')),
    # path('', views.index, name = 'index')
    # path("", views.index, name="index"),
]