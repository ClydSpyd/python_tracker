# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        serializer = UserSerializer(user)

        return Response({
            "message": "User created",  
            "user": serializer.data,
            },
            status=status.HTTP_201_CREATED
        )

# test GET route to return debug message
class DebugView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "HELLO WORLD"}, status=status.HTTP_200_OK)

# get all users
class UserListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all()
        if not users.exists():
            return Response({"message": "No users found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)