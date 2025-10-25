from django.urls import path

from .views import CheckInListCreateView, CheckinsByMonthView

urlpatterns = [
    path('', CheckInListCreateView.as_view(), name='checkin-list-create'),
    path('monthly/', CheckinsByMonthView.as_view(), name='checkins-by-month'),
]