from rest_framework import generics
from ..models import Link
from ..serializers import LinkSerializer
from rest_framework.permissions import IsAuthenticated
from users.authentication import CookieJWTAuthentication

class LinkListView(generics.ListAPIView):
    serializer_class = LinkSerializer
    queryset = Link.objects.all().order_by("url")

class LinkCreateView(generics.CreateAPIView):
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
