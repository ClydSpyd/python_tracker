from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from users.authentication import CookieJWTAuthentication
from .serializers import HabitSerializer, HabitWithRecordsSerializer
from .models import Habit, HabitRecord
from django.shortcuts import get_object_or_404
from datetime import datetime
from .services import get_user_habits_with_completions
from django.utils.timezone import now
from django.utils.timezone import localdate
from datetime import timedelta

class CreateHabitView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description")
        target = request.data.get("target")
        icon = request.data.get("icon")
        color_scheme = request.data.get("colorScheme")


        # Validate required fields
        if not title or not description or not target or not icon:
            return Response(
                {"error": "missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the habit using the serializer
        habit_data = {
            "title": title,
            "description": description,
            "target": target,
            "icon": icon,
            "color_scheme": color_scheme,
        }

        serializer = HabitSerializer(data=habit_data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "Habit created successfully", "habit": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ToggleHabitRecord(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request):
            print("Request query params:", request.data)
            habit_id = request.data.get("habit_id")
            date = request.data.get("date")  # Expected in 'YYYY-MM-DD' format

            print("Habit ID:", habit_id)
            print("Date:", date)

            if not habit_id or not date:
                return Response(
                    {"error": "habitId and date are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            habit = get_object_or_404(Habit, id=habit_id, user=request.user)

            print("Found habit:", habit)

            habit_record, created = HabitRecord.objects.get_or_create(
                habit=habit,
                date=date,
            )

            print("Habit record:", habit_record)

            if not created:
                # already exists -> delete it (toggle off)
                habit_record.delete()
                return Response(
                    {"message": "Habit marked as incomplete."},
                    status=status.HTTP_200_OK
                )

            # else, newly created (toggle on)
            return Response(
                {"message": "Habit marked as complete."},
                status=status.HTTP_201_CREATED
            )

class HabitListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        habits = Habit.objects.filter(user=request.user)
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class HabitDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request, habit_id):
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        serializer = HabitSerializer(habit)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, habit_id):
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        data = request.data.copy()
        # Map camelCase to snake_case for colorScheme from FE
        if "colorScheme" in data:
            data["color_scheme"] = data.pop("colorScheme")
        serializer = HabitSerializer(habit, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Habit updated successfully", "habit": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, habit_id):
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        habit.delete()
        return Response(
            {"message": "Habit deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    
class UserHabitsWithCompletionsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        start_date = request.query_params.get("start_date") 
        range_days = request.query_params.get("range_days") 

        # If no date given, default to today
        if start_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                return Response(
                    {"error": "Invalid start_date format. Expected YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            start_date = now().date()

        # If no range_days given, default to 7
        try:
            range_days = int(range_days) if range_days else 7  # default to 7
            if range_days < 1:
                raise ValueError
        except ValueError:
            return Response(
                {"error": "range_days must be a positive integer."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
        habits = get_user_habits_with_completions(request.user, start_date, range_days)

        serializer = HabitWithRecordsSerializer(habits, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserHabitStatsView(APIView):
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