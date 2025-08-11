# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.authentication import CookieJWTAuthentication
from rest_framework import generics
from .models import FocusItem
from .serializers import FocusItemSerializer

from django.utils.dateparse import parse_datetime

# 🔹 List + Create
class FocusItemListCreateView(generics.ListCreateAPIView):
    serializer_class = FocusItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return FocusItem.objects.filter(user=self.request.user).order_by('week_starting')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 🔹 Retrieve single item
class FocusItemDetailView(generics.RetrieveAPIView):
    serializer_class = FocusItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return FocusItem.objects.filter(user=self.request.user)

# 🔹 Update (PATCH/PUT)
class FocusItemUpdateView(generics.UpdateAPIView):
    serializer_class = FocusItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return FocusItem.objects.filter(user=self.request.user)

# 🔹 Delete
class FocusItemDeleteView(generics.DestroyAPIView):
    serializer_class = FocusItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return FocusItem.objects.filter(user=self.request.user)


class FocusItemClearAllView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def delete(self, request):
        deleted_count, _ = FocusItem.objects.filter(user=request.user).delete()
        return Response(
            {"message": f"Deleted {deleted_count} focus items."},
            status=status.HTTP_200_OK
        )

class FocusItemUpdateDateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def patch(self, request):
        new_date_str = request.data.get("week_starting")

        if not new_date_str:
            return Response({"error": "Missing 'week_starting' value."}, status=400)

        # Parse ISO 8601 datetime string (e.g. "2024-05-03T12:00:00Z")
        parsed_date = parse_datetime(new_date_str)

        if not parsed_date:
            return Response({"error": "Invalid datetime format."}, status=400)

        updated_count = FocusItem.objects.filter(user=request.user).update(week_starting=parsed_date)

        return Response(
            {"message": f"Updated {updated_count} focus items.", "new_week_starting": parsed_date},
            status=status.HTTP_200_OK
        )
