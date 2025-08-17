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

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    authors = models.JSONField(null=True, blank=True)
    cover = models.URLField(null=True, blank=True)
    edition_key = models.CharField(max_length=50, null=True, blank=True)
    olid = models.CharField(max_length=50, null=True, blank=True)
    work_key = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Books"
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_title')
        ]

class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Links"
        constraints = [
            models.UniqueConstraint(fields=['url'], name='unique_url')
        ]

class PinnedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=50)
    item_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item_type', 'item_id')
        verbose_name_plural = "Pinned Items"

    def __str__(self):
        return f"{self.user.username} pinned {self.item_type} with ID {self.item_id}"