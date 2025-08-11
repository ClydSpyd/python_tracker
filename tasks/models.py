from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('todo', 'To Do'), ('in_progress', 'In Progress'), ('blocked', 'Blocked'), ('complete', 'Complete')], default='todo')
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set at creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically set at creation and on each update
    completed_at = models.DateTimeField(null=True, blank=True)  # Nullable field for completed tasks

    def __str__(self):
        return self.title
