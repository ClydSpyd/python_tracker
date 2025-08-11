from django.urls import path

from .views import AddTaskView, UpdateTaskView, TaskListView

urlpatterns = [
    path("add/", AddTaskView.as_view(), name="add_task"),
    path("update/<int:task_id>/", UpdateTaskView.as_view(), name="update_task"),
    path("list/", TaskListView.as_view(), name="task_list"),
]