from django.db import models
from django.contrib.auth.models import User

class FocusItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='focus_items')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=False)
    week_starting = models.DateTimeField()
    icon = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        ordering = ['week_starting']
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='unique_focus_per_user')
        ]

    def __str__(self):
        return f"{self.user.username}: {self.title}"
