from rest_framework import generics
from ..models import PinnedItem, PinnedItem
from ..serializers import PinnedItemSerializer, PinnedItemEnrichedSerializer
from rest_framework.permissions import IsAuthenticated
from users.authentication import CookieJWTAuthentication
from rest_framework.exceptions import PermissionDenied

class PinnedItemListView(generics.ListAPIView):
    serializer_class = PinnedItemSerializer
    queryset = PinnedItem.objects.all().order_by("created_at")

class PinnedItemCreateView(generics.CreateAPIView):
    serializer_class = PinnedItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class PinnedItemEnrichedListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    serializer_class = PinnedItemEnrichedSerializer

    def get_queryset(self):
        return (
            PinnedItem.objects
            .filter(user=self.request.user)
            .order_by("created_at")
            .only("id", "item_type", "item_id", "created_at", "user")  # lean fetch
        )

class PinnedItemDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    queryset = PinnedItem.objects.all()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this item.")
        instance.delete()