from django.urls import path
from .views import HabitCompletionStatsView, MentalCheckinStatsView, WeekAtGlanceStatsView

urlpatterns = [
    path('habit-completion/', HabitCompletionStatsView.as_view(), name='habit-completion-stats'),
    path('mental-checkin/', MentalCheckinStatsView.as_view(), name='mental-checkin-stats'),
    path('week-glance/', WeekAtGlanceStatsView.as_view(), name='week-at-glance-stats'),
]