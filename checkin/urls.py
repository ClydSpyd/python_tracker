from django.urls import path

from .views import CheckInListCreateView

urlpatterns = [
    path('', CheckInListCreateView.as_view(), name='checkin-list-create'),
]