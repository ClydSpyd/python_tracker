from django.urls import path
from .views import (search_omdb, MovieListView, MediaCreateView, QuoteCreateView, QuoteListView, WikiItemsListView, BookSearchView, BookSaveView)

urlpatterns = [
    path("", WikiItemsListView.as_view(), name="wiki_items_list"),
    path("media/add/", MediaCreateView.as_view(), name="media_add"),
    path("quotes/add/", QuoteCreateView.as_view(), name="quote_add"),
    path("books/add/", BookSaveView.as_view(), name="book_add"),
    path("movies/", MovieListView.as_view(), name="movie_list"),
    path("quotes/", QuoteListView.as_view(), name="quote_list"),
    path("omdb/search/", search_omdb, name="search_omdb"),
    path("books/search/", BookSearchView.as_view(), name="book_search"),
]
