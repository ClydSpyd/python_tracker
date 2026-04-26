from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.authentication import CookieJWTAuthentication
from .models import Activity
from .serializers import ActivitySerializer

# List all activities (admin/global)
from rest_framework.permissions import IsAdminUser

# List all activities (admin/global)
class AllActivityListView(generics.ListAPIView):
	serializer_class = ActivitySerializer
	# permission_classes = [IsAuthenticated]
	# authentication_classes = [CookieJWTAuthentication]
	permission_classes = [IsAdminUser]

	def get_queryset(self):
		return Activity.objects.all().order_by('-date')

# List and Create Activities
class ActivityListCreateView(generics.ListCreateAPIView):
	serializer_class = ActivitySerializer
	permission_classes = [IsAuthenticated]
	authentication_classes = [CookieJWTAuthentication]

	def get_queryset(self):
		date_param = self.request.query_params.get('date', None)
		if date_param:
			return Activity.objects.filter(user=self.request.user, date=date_param).order_by('-date')
		return Activity.objects.filter(user=self.request.user).order_by('-date')

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

# Retrieve, Update, and Delete a single Activity
class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = ActivitySerializer
	permission_classes = [IsAuthenticated]
	authentication_classes = [CookieJWTAuthentication]

	def get_queryset(self):
		return Activity.objects.filter(user=self.request.user)
