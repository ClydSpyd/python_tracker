from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.authentication import CookieJWTAuthentication
from rest_framework import status

from ..models import Movie, Series, Quote, Book, Link
from ..serializers import MovieSerializer, SeriesSerializer, QuoteSerializer, BookSerializer, LinkSerializer

TYPE_TO_MODEL = {
    "book": Book,
    "movie": Movie,
    "series": Series,
    "quote": Quote,
}

class WikiItemsListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        user = request.user
        movies = MovieSerializer(Movie.objects.filter(user=user), many=True).data
        series = SeriesSerializer(Series.objects.filter(user=user), many=True).data
        quotes = QuoteSerializer(Quote.objects.filter(user=user), many=True).data
        books  = BookSerializer(Book.objects.filter(user=user), many=True).data
        links  = LinkSerializer(Link.objects.filter(user=user), many=True).data

        for m in movies: m["type"] = "movie"
        for s in series: s["type"] = "series"
        for q in quotes: q["type"] = "quote"
        for b in books:  b["type"] = "book"
        for l in links:  l["type"] = "link"

        combined = movies + series + quotes + books + links
        combined.sort(key=lambda x: x.get("created_at"), reverse=True)
        return Response(combined)

class WikiDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def delete(self, request, item_type: str, pk: str):
        item_type = (item_type or "").lower()
        Model = TYPE_TO_MODEL.get(item_type)
        if not Model:
            return Response({"detail": f"Unknown type: {item_type}"}, status=400)

        # if PKs are UUIDs, this still works; if ints, it’s fine too.
        obj = Model.objects.filter(pk=pk, user=request.user).first()
        if not obj:
            return Response({"detail": "Not found."}, status=404)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
