from rest_framework.permissions import IsAuthenticated
from users.authentication import CookieJWTAuthentication
from rest_framework import generics
from .models import Idea
from .serializers import IdeaSerializer

# 🔹 List + Create
class IdeaListCreateView(generics.ListCreateAPIView):
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return Idea.objects.filter(user=self.request.user).order_by('created_at')

    def perform_create(self, serializer):
        print("Data received:", serializer.validated_data)
        serializer.save(user=self.request.user)

# 🔹 Retrieve single item
class IdeaDetailView(generics.RetrieveAPIView):
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return Idea.objects.filter(user=self.request.user)

# 🔹 Update (PATCH/PUT)
class IdeaUpdateView(generics.UpdateAPIView):
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return Idea.objects.filter(user=self.request.user)

# 🔹 Delete
class IdeaDeleteView(generics.DestroyAPIView):
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return Idea.objects.filter(user=self.request.user)
 