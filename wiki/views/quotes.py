from rest_framework import generics
from ..models import Quote
from ..serializers import QuoteSerializer
from rest_framework.permissions import IsAuthenticated
from users.authentication import CookieJWTAuthentication

class QuoteListView(generics.ListAPIView):
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all().order_by("content")

class QuoteCreateView(generics.CreateAPIView):
    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
