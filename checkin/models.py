from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkins')
    date = models.DateField()
    mood = models.IntegerField(validators=[MaxValueValidator(5)])
    energy_level =  models.IntegerField(validators=[MaxValueValidator(100)])
    focus_level = models.IntegerField(validators=[MaxValueValidator(100)])
    stress_level = models.IntegerField(validators=[MaxValueValidator(100)])
    reflection = models.TextField(null=True, blank=True)
    mental_state = models.CharField(max_length=24, null=True, blank=True)

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(fields=['user', 'date'], name='unique_checkin_per_user_per_day')
        ]

    def __str__(self):
        return f"{self.user.username} - checkin {self.date}"