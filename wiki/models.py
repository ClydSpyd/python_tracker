from django.db import models
from django.contrib.auth.models import User

class MediaBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4, null=True, blank=True)
    released = models.CharField(max_length=20, null=True, blank=True)
    runtime = models.CharField(max_length=20, null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    director = models.CharField(max_length=255, null=True, blank=True)
    actors = models.CharField(max_length=255, null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    metascore = models.CharField(max_length=10, null=True, blank=True)
    imdb_rating = models.CharField(max_length=10, null=True, blank=True)
    imdb_votes = models.CharField(max_length=20, null=True, blank=True)
    imdb_id = models.CharField(max_length=20, unique=True)
    ratings = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Movie(MediaBase):
    class Meta(MediaBase.Meta):
        ordering = ['title']
        verbose_name_plural = "Movies"
        constraints = [
            models.UniqueConstraint(fields=['imdb_id'], name='unique_imdb_id')
        ]

    def __str__(self):
        return self.title

class Series(MediaBase):
    class Meta(MediaBase.Meta):
        ordering = ['title']
        verbose_name_plural = "Series"
        constraints = [
            models.UniqueConstraint(fields=['imdb_id'], name='unique_series_imdb_id')
        ]

    def __str__(self):
        return self.title

class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotes')
    content = models.TextField()
    author = models.CharField(max_length=255)
    additional_info = models.TextField(null=True, blank=True)
    year = models.CharField(max_length=4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.content}" - {self.author if self.author else "Unknown"}'
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Quote"
        constraints = [
            models.UniqueConstraint(fields=['content', 'author'], name='unique_quote')
        ]