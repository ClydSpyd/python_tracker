from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    title = models.CharField(max_length=200)
    description = models.TextField()
    target = models.IntegerField()  # Target times per week
    icon = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class HabitRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='records')
    date = models.DateField(default=date.today)  # the date the habit was completed

    class Meta:
        unique_together = ('habit', 'date')  # One record per habit per day

    def __str__(self):
        return f"{self.habit.title} on {self.date}"
