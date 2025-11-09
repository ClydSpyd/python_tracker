from django.urls import path
from .views import SpaceListCreateView

urlpatterns = [
    path('', SpaceListCreateView.as_view(), name='space-list-create'),
]       