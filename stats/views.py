from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from users.authentication import CookieJWTAuthentication
from habits.models import Habit, HabitRecord
from django.utils.timezone import now
from django.utils.timezone import localdate
from datetime import timedelta

# Create your views here.
class HabitCompletionStatsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):

        today = localdate()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        habits = Habit.objects.filter(user=request.user)
        total_target = sum(habit.target for habit in habits)

        completions = HabitRecord.objects.filter(
            habit__in=habits,
            date__range=[start_of_week, end_of_week]
        ).count()

        return Response(
            {
                "total_target": total_target,
                "total_completions_this_week": completions
            },
            status=status.HTTP_200_OK
        )

class MentalCheckinStatsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        from checkin.models import CheckIn
        from django.db.models import Avg

        today = localdate()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        checkins = CheckIn.objects.filter(
            user=request.user,
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

        return Response(
            {
                "number_of_checkins": checkins.count(),
                "mood_per_day": mood_per_day,
                "average_mood": avg_mood,
                "average_energy_level": avg_energy,
                "energy_per_day": energy_per_day,
                "average_focus_level": avg_focus,
                "focus_per_day": focus_per_day,
                "average_stress_level": avg_stress,
                "stress_per_day": stress_per_day
            },
            status=status.HTTP_200_OK
        )