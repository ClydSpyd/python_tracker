# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer, MyTokenObtainPairSerializer, UserSerializer
from .authentication import CookieJWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django.utils.dateparse import parse_datetime

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Custom Token Refresh View to handle JWT refresh tokens in cookies
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "No refresh token"}, status=400)
        # Inject refresh token into request data
        request.data["refresh"] = refresh_token

        try:
            response = super().post(request, *args, **kwargs)
        except AuthenticationFailed:
            # Catch the exception and return 400 instead of 401 to avoid FE interceptor loop
            return Response({"detail": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        
        if response.status_code == 200 and "access" in response.data:
            access_token = response.data["access"]
            cookie_response = Response({"access": access_token}, status=200)
            cookie_response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="None",
                path="/",
                max_age=15 * 60,  # 15 minutes
            )
            return cookie_response
        return response


# POST Register a new user
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

# POST Login
class LoginView(TokenObtainPairView):

    # custom serializer to augment TokenObtainPairSerializer class
    # add custom claims to the token
    # serializer_class = MyTokenObtainPairSerializer

    # custom serializer to alter TokenObtainPairSerializer class
    # add custom default_error_message
    serializer_class = CustomTokenObtainPairSerializer


    def post(self, request, *args, **kwargs):
        
        # super is used to call the parent class method
        # in this case, TokenObtainPairView, augmented by my serializer_class
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Retrieve the user from the serializer's validated data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            serialized_user = UserSerializer(user)

            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")
            cookie_response = Response({
                "message": "Login successful", 
                "user": serialized_user.data
                }, status=status.HTTP_200_OK)
            
            cookie_response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="None",
                path="/",
                max_age=15 * 60,  # 15 minutes
            )
            
            cookie_response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="None",
                path="/",
                max_age=7 * 24 * 60 * 60,  # 7 days
            )
            return cookie_response

        print(response.data)
        return response

# GET route to return user info based on token
class UserInfoView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# POST logout and remove http-only cookies
class LogoutView(APIView):    
    # authentication_classes = [CookieJWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.set_cookie(
            key="access_token",
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
        )
        response.set_cookie(
            key="refresh_token",
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
        )
        return response

# GET route to return debug message
class DebugView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "HELLO WORLD"}, status=status.HTTP_200_OK)

# GET all users
class UserListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all()
        if not users.exists():
            return Response({"message": "No users found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    