from django.urls import path
from .views import HabitCompletionStatsView, MentalCheckinStatsView

urlpatterns = [
    path('habit-completion/', HabitCompletionStatsView.as_view(), name='habit-completion-stats'),
    path('mental-checkin/', MentalCheckinStatsView.as_view(), name='mental-checkin-stats'),
]