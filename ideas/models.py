from django.db import models
from django.contrib.auth.models import User


class Idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ideas')
    title = models.CharField(max_length=255)
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='unique_idea_per_user')
        ]

    def __str__(self):
        return f"{self.user.username}: {self.title}"

# Create your models here.
