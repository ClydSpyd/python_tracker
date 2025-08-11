from django.urls import path
from .views import (search_omdb, MovieListView, MovieCreateView)

urlpatterns = [
    path("omdb/search/", search_omdb, name="search_omdb"),
    path("movies/", MovieListView.as_view(), name="movie_list"),
    path("movies/add/", MovieCreateView.as_view(), name="movie_add")
]
