from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    RegisterView, 
    DebugView, 
    UserListView, 
    LogoutView, 
    LoginView, 
    UserInfoView,
    CookieTokenRefreshView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("debug/", DebugView.as_view(), name="debug"),
    path("users/", UserListView.as_view(), name="user_list"),

    # JWT cookie-based auth
    path("login/", LoginView.as_view(), name="login"),
    path("me/", UserInfoView.as_view(), name="user_info"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
