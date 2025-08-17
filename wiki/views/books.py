from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.authentication import CookieJWTAuthentication

from ..serializers import BookSerializer
from ..services.openlibrary_client import search_books, fetch_work_description
from django.db import transaction

class BookSearchView(APIView):
    def get(self, request):
        q = (request.GET.get("q") or "").strip()
        if not q:
            return Response({"detail": "Missing query param: q"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            limit = int(request.GET.get("limit", 20))
        except ValueError:
            limit = 20

        try:
            results = search_books(q, limit)
        except Exception as e:
            return Response({"detail": f"Upstream error: {e}"}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(results)


class BookSaveView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    @transaction.atomic
    def post(self, request):
        payload = request.data.copy()
        desc = fetch_work_description(payload.get("work_key"))
        if desc:
            payload["description"] = desc

        ser = BookSerializer(data=payload, context={"request": request})
        ser.is_valid(raise_exception=True)
        book = ser.save(user=request.user)
        return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
