from django.urls import path
from .views import CreateHabitView, ToggleHabitRecord, HabitListView, HabitDetailView, UserHabitsWithCompletionsView

urlpatterns = [
    path("<int:habit_id>/", HabitDetailView.as_view(), name="habit_detail_GET_PATCH"),
    path("add/", CreateHabitView.as_view(), name="create_habit"),
    path("toggle/", ToggleHabitRecord.as_view(), name="toggle_habit_completion"),
    path("list/", HabitListView.as_view(), name="habit_list"),
    path("activity/", UserHabitsWithCompletionsView.as_view(), name="user_habits_with_completions"),
]