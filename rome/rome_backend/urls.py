from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # This maps the root of /rome_backend/ to the index view
]