from rest_framework import generics
from .models import CheckIn
from .serializers import CheckInSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.authentication import CookieJWTAuthentication
from datetime import date


class CheckInListCreateView(generics.ListCreateAPIView):
    serializer_class = CheckInSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        date_param = self.request.query_params.get('date', None)
        if date_param:
            return CheckIn.objects.filter(user=self.request.user, date=date_param).order_by('-date')
        return CheckIn.objects.filter(user=self.request.user).order_by('-date')

    def create(self, request, *args, **kwargs):
        today = request.query_params.get('date', date.today())
        checkin, created = CheckIn.objects.get_or_create(
            user=request.user,
            date=today,
            defaults=request.data
        )
        if not created:
            # Update the existing check-in
            serializer = self.get_serializer(checkin, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(checkin)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class CheckinsByMonthView(generics.ListAPIView):
    serializer_class = CheckInSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        year = int(request.query_params.get('year'))
        month = int(request.query_params.get('month'))
        checkins = CheckIn.objects.filter(
            user=request.user,
            date__year=year,
            date__month=month
        ).order_by('-date')
        print(f"checkins: {checkins}")
        dates = [str(checkin.date) for checkin in checkins]
        return Response(dates, status=status.HTTP_200_OK)