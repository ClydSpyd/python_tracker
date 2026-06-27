from django.urls import path
from wiki.views import (
    search_omdb, 
    MediaCreateView, 
    QuoteCreateView, QuoteListView, 
    WikiItemsListView, 
    BookSearchView, 
    BookSaveView,
    BookDetailsView,
    LinkCreateView,
    LinkListView,
    PinnedItemCreateView,
    PinnedItemListView,
    PinnedItemEnrichedListView,
    MediaDetailsView,
    PinnedItemDeleteView
    )
from wiki.views.quotes import DeleteQuoteView

urlpatterns = [
    path("", WikiItemsListView.as_view(), name="wiki_items_list"),
    path("media/", MediaCreateView.as_view(), name="media_add_or_delete"),
    path("media/<int:pk>/", MediaDetailsView.as_view(), name="media_details"),
    path("quotes/add/", QuoteCreateView.as_view(), name="quote_add"),
    path("quotes/delete/<int:pk>/", DeleteQuoteView.as_view(), name="quote_delete"),
    path("books/", BookSaveView.as_view(), name="book_add_or_delete"),
    path("books/search/", BookSearchView.as_view(), name="book_search"),
    path("books/<int:pk>/", BookDetailsView.as_view(), name="book_details"),
    path("quotes/", QuoteListView.as_view(), name="quote_list"),
    path("omdb/search/", search_omdb, name="search_omdb"),
    path("links/add/", LinkCreateView.as_view(), name="link_add"),
    path("links/", LinkListView.as_view(), name="link_list"),
    path("pinned-items/add/", PinnedItemCreateView.as_view(), name="pinned_item_add"),
    path("pinned-items/", PinnedItemListView.as_view(), name="pinned_item_list"),
    path("pinned-items/enriched/", PinnedItemEnrichedListView.as_view(), name="pinned_item_enriched_list"),
    path("pinned-items/delete/<int:pk>/", PinnedItemDeleteView.as_view(), name="pinned_item_delete"),

]
