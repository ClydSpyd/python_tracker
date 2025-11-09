from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from users.authentication import CookieJWTAuthentication
from rest_framework import generics
from .models import Space
from .serializers import SpaceSerializer

# 🔹 List + Create
class SpaceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    def get_queryset(self):
        return Space.objects.filter(user=self.request.user).order_by('created_at')  