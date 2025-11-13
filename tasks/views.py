from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from users.authentication import CookieJWTAuthentication
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404
from .models import Task

class AddTaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description")

        # Validate required fields
        if not title or not description:
            return Response(
                {"error": "Both 'title' and 'description' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task_status = request.data.get("status", "todo")

        # Create the task using the serializer
        task_data = {
            "title": title,
            "description": description,
            "status": task_status
        }

        serializer = TaskSerializer(data=task_data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "Task created successfully", "task": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateTaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def patch(self, request, task_id):
        # Fetch the existing task
        task = get_object_or_404(Task, id=task_id)

        # Initialize serializer with existing instance and incoming data
        serializer = TaskSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Task updated successfully", "task": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class DeleteTaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def delete(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
        return Response(
            {"message": "Task deleted successfully"},
            status=status.HTTP_200_OK
        )   
    