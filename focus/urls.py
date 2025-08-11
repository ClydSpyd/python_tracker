from django.urls import path
from .views import (
    FocusItemListCreateView,
    FocusItemUpdateView,
    FocusItemDeleteView,
    FocusItemClearAllView,
    FocusItemUpdateDateView
)

urlpatterns = [
    path('', FocusItemListCreateView.as_view(), name='focus-list-create'),
    path('<int:pk>/', FocusItemUpdateView.as_view(), name='focus-update'),
    path('<int:pk>/delete/', FocusItemDeleteView.as_view(), name='focus-delete'),
    path('clear/', FocusItemClearAllView.as_view(), name='focus-clear-all'),
    path('update-date/', FocusItemUpdateDateView.as_view(), name='focus-update-date'),
]
