from django.urls import path
from .views import ActivityListCreateView, ActivityDetailView, AllActivityListView

urlpatterns = [
    path('', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('all/', AllActivityListView.as_view(), name='activity-list-all'),
    path('<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),
]
