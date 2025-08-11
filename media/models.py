from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies')
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    imdb_id = models.CharField(max_length=20, unique=True)
    poster = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Movies"
        constraints = [
            models.UniqueConstraint(fields=['imdb_id'], name='unique_imdb_id')
        ]