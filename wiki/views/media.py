from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from users.authentication import CookieJWTAuthentication
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
from django.conf import settings

from ..models import Movie, Series, Book
from ..serializers import MovieSerializer, SeriesSerializer, BookSerializer
from ..services.omdb_client import fetch_by_imdb_id, map_omdb_payload, OmdbError

class MediaListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all().order_by("title")


class MediaCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    @transaction.atomic
    def post(self, request):
        item_type = (request.data.get("type") or "movie").lower()
        imdb_id = request.data.get("imdbId") or request.data.get("imdb_id")
        if not imdb_id:
            return Response({"detail": "imdbId is required."}, status=400)

        try:
            omdb = fetch_by_imdb_id(imdb_id)
        except OmdbError as e:
            return Response({"detail": str(e)}, status=400)

        payload = map_omdb_payload(omdb, imdb_id)
        serializer_class = SeriesSerializer if item_type == "series" else MovieSerializer
        ser = serializer_class(data=payload, context={"request": request})
        ser.is_valid(raise_exception=True)
        obj = ser.save(user=request.user)
        return Response(serializer_class(obj).data, status=status.HTTP_201_CREATED)
    
    @transaction.atomic
    def delete(self, request):
        item_type = (request.data.get("type") or request.query_params.get("type") or "movie").lower()
        imdb_id = request.data.get("imdbId") or request.data.get("imdb_id") or request.query_params.get("imdbId") or request.query_params.get("imdb_id")

        print("DELETE media request:", item_type, imdb_id)
        if not imdb_id:
            return Response({"detail": "imdbId is required."}, status=400)

        model = Series if item_type == "series" else Movie
        try:
            obj = model.objects.get(imdb_id=imdb_id, user=request.user)
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except model.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

# retreive, update, delete individual media tiems
class MediaDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    
    def get_serializer_class(self):
        item_type = self.request.query_params.get("type", "movie").lower()
        if item_type == "series":
            return SeriesSerializer
        if item_type == "book":
            return BookSerializer
        return MovieSerializer

    def get_queryset(self):
        type_param = self.request.query_params.get("type", "movie").lower()
        if type_param == "series":
            model = Series
        elif type_param == "book":
            model = Book
        else:
            model = Movie
        print("MediaDetailsView get_queryset called" + f"with type={type_param} for user {self.request.user}")
        return model.objects.order_by("title")

@csrf_exempt
@require_GET
def search_omdb(request):
    api_key = getattr(settings, "OMDB_API_KEY", None)
    if not api_key:
        return JsonResponse({"error": "OMDB_API_KEY not configured"}, status=500)

    base = f"http://www.omdbapi.com/?apikey={api_key}"
    query_string = request.META.get("QUERY_STRING", "")
    url = f"{base}&{query_string}" if query_string else base
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

    if data.get("Response") == "False":
        return JsonResponse({"Search": []}, safe=False)
    
    if "Search" in data:
        seen = set()
        filtered = []
        for item in data["Search"]:
            imdb_id = item.get("imdbID")
            if imdb_id and imdb_id not in seen:
                seen.add(imdb_id)
                filtered.append(item)
        data["Search"] = filtered
    
    return JsonResponse(data, safe=False)
