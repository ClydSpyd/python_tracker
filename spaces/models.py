from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Space(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spaces')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.JSONField(default=list, blank=True, null=True)


    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='unique_user_space_title')
        ]

    def __str__(self):
        return f"{self.user.username} - space {self.title}"