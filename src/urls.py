from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/habits/', include('habits.urls')),
    path('api/focus/', include('focus.urls')),
    path("api/wiki/", include("wiki.urls")),
    path("api/checkin/", include("checkin.urls")),
    path("api/stats/", include("stats.urls")),
    path("api/ideas/", include("ideas.urls")),
    path("api/spaces/", include("spaces.urls")),
]
