from django.contrib import admin
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'year', 'imdb_id', 'user']
    search_fields = ['title', 'imdb_id', 'user__username']
    readonly_fields = ['user']
    list_filter = ['user'] 

admin.site.register(Movie, MovieAdmin)
