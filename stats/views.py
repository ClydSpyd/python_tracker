from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from habits.services import get_user_habits_with_completions
from users.authentication import CookieJWTAuthentication
from django.utils.timezone import now
from django.utils.timezone import localdate
from datetime import timedelta
from habits.serializers import HabitWithRecordsSerializer
from checkin.models import CheckIn
from django.db.models import Avg

def get_habit_stats(user, week_offset=0):
    today = localdate()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    habits_with_records = get_user_habits_with_completions(user, start_of_week, 7)
    serializer = HabitWithRecordsSerializer(habits_with_records, many=True)
    return_habits = []
    for habit in serializer.data:
        title = habit.get('title')
        target = habit.get('target', 0)
        records = habit.get('records', [])
        return_habits.append({
            "title": title,
            "target": target,
            "completions": records
        })
    return return_habits

def get_checkin_stats(user, week_offset=0):
    today = localdate()
    # Start week on Monday
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=6)
    checkins = CheckIn.objects.filter(
        user=user,
        date__range=[start_of_week, end_of_week]
    )
    mood_per_day = []
    energy_per_day = []
    focus_per_day = []
    stress_per_day = []
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        checkin = checkins.filter(date=day).first()
        mood_per_day.append(checkin.mood if checkin else None)
        energy_per_day.append(checkin.energy_level if checkin else None)
        focus_per_day.append(checkin.focus_level if checkin else None)
        stress_per_day.append(checkin.stress_level if checkin else None)
    avg_mood = checkins.aggregate(Avg('mood'))['mood__avg']
    avg_energy = checkins.aggregate(Avg('energy_level'))['energy_level__avg']
    avg_focus = checkins.aggregate(Avg('focus_level'))['focus_level__avg']
    avg_stress = checkins.aggregate(Avg('stress_level'))['stress_level__avg']
    return {
        "number_of_checkins": checkins.count(),
        "mood_per_day": mood_per_day,
        "average_mood": avg_mood,
        "average_energy_level": avg_energy,
        "energy_per_day": energy_per_day,
        "average_focus_level": avg_focus,
        "focus_per_day": focus_per_day,
        "average_stress_level": avg_stress,
        "stress_per_day": stress_per_day
    }

class WeekAtGlanceStatsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        week_offset = int(request.query_params.get('week_offset', 0))
        print("Week Offset:", week_offset)
        habit_stats = get_habit_stats(request.user, week_offset)
        checkin_stats = get_checkin_stats(request.user, week_offset)
        return Response(
            {
                "habits": habit_stats,
                "checkins": checkin_stats
            },
            status=status.HTTP_200_OK
        )
    
class HabitCompletionStatsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        stats = get_habit_stats(request.user)
        return Response(stats, status=status.HTTP_200_OK)

class MentalCheckinStatsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        stats = get_checkin_stats(request.user)
        return Response(stats, status=status.HTTP_200_OK)