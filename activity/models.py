from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=100)  # e.g. "cardio", "strength", "sport"
    time = models.CharField(max_length=5)  # e.g. "18:30"
    duration = models.IntegerField()  # duration in minutes
    icon = models.CharField(max_length=100)  # icon name for FE to render
    colorConfig = models.IntegerField()  # idx for selected color scheme in FE colorCombos array
    location = models.CharField(max_length=200)
    distance = models.FloatField(null=True, blank=True)  # optional distance in km
    kcals = models.IntegerField(null=True, blank=True)  # optional calories burned
    date = models.DateField(default=date.today)  # the date the activity was completed
    created_at = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)  # optional description or notes about the activity

    def __str__(self):
        return self.title