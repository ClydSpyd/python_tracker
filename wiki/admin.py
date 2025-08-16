from django.contrib import admin
from .models import Movie, Series, Quote, Book

class MovieAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'year', 'imdb_id', 'user']
    search_fields = ['title', 'imdb_id', 'user__username']
    readonly_fields = ['user', 'imdb_id']
    list_filter = ['user'] 

admin.site.register(Movie, MovieAdmin)

class SeriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'year', 'imdb_id', 'user']
    search_fields = ['title', 'imdb_id', 'user__username']
    readonly_fields = ['user', 'imdb_id']
    list_filter = ['user']  

admin.site.register(Series, SeriesAdmin)

class QuoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'author', 'user', 'year']
    search_fields = ['content', 'author', 'user__username', 'year']
    readonly_fields = ['user']
    list_filter = ['user']

admin.site.register(Quote, QuoteAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'olid', 'user']
    search_fields = ['title', 'olid', 'user__username']
    readonly_fields = ['user', 'olid']
    list_filter = ['user']

admin.site.register(Book, BookAdmin)
