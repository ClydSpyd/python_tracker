from datetime import timedelta
from django.utils.timezone import now
from .models import Habit, HabitRecord
from django.db.models import Prefetch, Q


def get_week_date_range(target_date=None):
    if not target_date:
        target_date = now().date()
    start_of_week = target_date - timedelta(days=target_date.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    return start_of_week, end_of_week


def get_user_habits_with_completions(user, start_date, range_days):
    """
    Given a start_date (date object), returns the user's habits
    and their HabitRecords from start_date (inclusive) for the next X days.
    """
    end_date = start_date + timedelta(days=range_days - 1)

    habit_records_qs = HabitRecord.objects.filter(date__range=(start_date, end_date))

    habits = Habit.objects.filter(
            user=user,
            enabled_at__lte=end_date,
        ).filter(
            Q(disabled_at__isnull=True) | Q(disabled_at__gt=start_date)
        ).prefetch_related(
            Prefetch('records', queryset=habit_records_qs)
        )

    return habits