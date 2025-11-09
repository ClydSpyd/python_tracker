from django.urls import path
from .views import IdeaListCreateView, IdeaUpdateView, IdeaDeleteView, IdeaDetailView

urlpatterns = [
    path('', IdeaListCreateView.as_view(), name='idea-list-create'),
    path('<int:pk>/', IdeaDetailView.as_view(), name='idea-detail'),
    path('<int:pk>/update/', IdeaUpdateView.as_view(), name='idea-update'),
    path('<int:pk>/delete/', IdeaDeleteView.as_view(), name='idea-delete'),
]