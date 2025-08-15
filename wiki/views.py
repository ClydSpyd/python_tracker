import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .serializers import MovieSerializer, SeriesSerializer, QuoteSerializer
from .models import Movie, Series, Quote
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.authentication import CookieJWTAuthentication
from django.db import transaction

OMDB_API_KEY = '9d4b151c'

class MovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return Movie.objects.filter().order_by('title')

class MediaCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def fetch_movie_data(self, imdb_id: str) -> dict:
        api_key = OMDB_API_KEY
        if not api_key:
            raise ValueError("Server misconfiguration: OMDB_API_KEY not set.")

        try:
            r = requests.get(
                "http://www.omdbapi.com/",
                params={"apikey": api_key, "i": imdb_id, "plot": "full"},
                timeout=6,
            )
            r.raise_for_status()
        except requests.RequestException as e:
            raise ValueError(f"Could not reach movie service: {e}")

        data = r.json()
        print(f"OMDB API response: {data}")  # Debugging line
        if data.get("Response") == "False":
            raise ValueError(data.get("Error") or "Movie not found")
        return data

    @staticmethod
    def to_int(s):
        try:
            return int(str(s).replace(',', ''))
        except Exception:
            return None
        
    def map_omdb(self, omdb: dict, imdb_id: str) -> dict:
        def to_int(s):
            try:
                return int(s)
            except Exception:
                return None
            
        print(f"Mapping OMDB data for IMDb ID: {imdb_id}") 

        payload = {
            "imdb_id": imdb_id,
            "title": omdb.get("Title"),
            "year": to_int(omdb.get("Year", "")),
            "released": omdb.get("Released"),
            "runtime": to_int((omdb.get("Runtime") or "").split()[0]),
            "genre": omdb.get("Genre"),
            "director": omdb.get("Director"),
            "actors": omdb.get("Actors"),
            "plot": omdb.get("Plot"),
            "language": omdb.get("Language"),
            "poster_url": omdb.get("Poster"),
            "metascore": self.to_int(omdb.get("Metascore")),
            "ratings": omdb.get("Ratings", []),
            "imdb_rating": (
                float(omdb["imdbRating"])
                if omdb.get("imdbRating") not in (None, "N/A")
                else None
            ),
            "imdb_votes": self.to_int(omdb.get("imdbVotes")),
        }

        print(f"Mapped payload: {payload}")  # Debugging line
        return payload

    @transaction.atomic
    def post(self, request):
        item_type = request.data.get("type", "movie").lower()
        imdb_id = request.data.get("imdbId") or request.data.get("imdb_id")

        print(f"TYPE: {item_type}, IMDB ID: {imdb_id}")  # Debugging line
        if not imdb_id:
            return Response({"detail": "imdbId is required."}, status=400)

        try:
            omdb = self.fetch_movie_data(imdb_id)
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)

        payload = self.map_omdb(omdb, imdb_id)

        if item_type == "series":
            serializer_class = SeriesSerializer
        else:
            serializer_class = MovieSerializer

        serializer = serializer_class(data=payload, context={"request": request})
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(user=request.user)

        return Response(serializer_class(obj).data, status=status.HTTP_201_CREATED)
    

@csrf_exempt
@require_GET
def search_omdb(request):
    if not OMDB_API_KEY:
        return JsonResponse({"error": "OMDB_API_KEY not configured"}, status=500)

    query_string = request.META.get("QUERY_STRING", "")

    base_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}"
    if query_string:
        target_url = f"{base_url}&{query_string}"
    else:
        target_url = base_url

    try:
        response = requests.get(target_url, timeout=5)
        print(f"OMDB API request: {target_url}")  # Debugging line
        print(f"OMDB API response status: {response.status_code}")  # Debugging line
        print(f"OMDB API response data: {response.text}")  # Print entire response data
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

    # If no results, return empty list
    if "Response" in data and data["Response"] == "False":
        return JsonResponse({"Search": []}, safe=False)

    return JsonResponse(data, safe=False)


class QuoteListView(generics.ListAPIView):
    serializer_class = QuoteSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [CookieJWTAuthentication]

    # def get_queryset(self):
    #     return Quote.objects.filter(user=self.request.user).order_by('-id')
    

    def get_queryset(self):
        return Quote.objects.filter().order_by('content')
    
class QuoteCreateView(generics.CreateAPIView):
    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WikiItemsListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        quotes = Quote.objects.all()
        series = Series.objects.all()

        # Serialize
        movie_data = MovieSerializer(movies, many=True).data
        quote_data = QuoteSerializer(quotes, many=True).data
        series_data = SeriesSerializer(series, many=True).data

        # Add a type field for sorting and identification
        for m in movie_data:
            m['type'] = 'movie'
        for q in quote_data:
            q['type'] = 'quote'
        for s in series_data:
            s['type'] = 'series'

        # Combine and sort by 'created_at'
        combined = movie_data + quote_data + series_data
        combined_sorted = sorted(combined, key=lambda x: x.get('created_at'), reverse=True)

        return Response(combined_sorted)
    

# views.py
from urllib.parse import urlencode
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

OPENLIB_SEARCH = "https://openlibrary.org/search.json"
COVER_BASE = "https://covers.openlibrary.org/b"

# Order of preference for building a cover URL
def build_cover_url(doc):
    # 1) cover_i
    cover_i = doc.get("cover_i")
    if isinstance(cover_i, int):
        return f"{COVER_BASE}/id/{cover_i}-M.jpg"

    # 2) cover_edition_key (OLID)
    olid = doc.get("cover_edition_key")
    if isinstance(olid, str):
        return f"{COVER_BASE}/olid/{olid}-M.jpg"

    # 3) first ISBN
    isbns = doc.get("isbn") or []
    if isinstance(isbns, list) and isbns:
        return f"{COVER_BASE}/isbn/{isbns[0]}-M.jpg"

    return None


class BookSearchView(APIView):
    """
    GET /api/books/search?q=<text>&limit=20
    Returns a trimmed list of books with a `cover` URL if available.
    """

    def get(self, request):
        q = (request.GET.get("q") or "").strip()
        if not q:
            return Response({"detail": "Missing query param: q"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            limit = int(request.GET.get("limit", 20))
        except ValueError:
            limit = 20

        fields = ",".join([
            "key",
            "title",
            "author_name",
            "first_publish_year",
            "cover_i",
            "cover_edition_key",
            "edition_key",
            "isbn",
        ])

        params = {
            "q": q,
            "limit": limit,
            "fields": fields,
        }

        try:
            r = requests.get(OPENLIB_SEARCH, params=params, timeout=6)
            r.raise_for_status()
        except requests.RequestException as e:
            return Response({"detail": f"Upstream error: {e}"}, status=status.HTTP_502_BAD_GATEWAY)

        payload = r.json()
        docs = payload.get("docs", [])

        results = []
        for d in docs:
            results.append({
                "title": d.get("title"),
                "authors": d.get("author_name") or [],
                "year": d.get("first_publish_year"),
                "cover": build_cover_url(d),
                "work_key": d.get("key"),
                "olid": d.get("cover_edition_key"),
                "edition_key": (d.get("edition_key") or [None])[0],
            })

        return Response({
            "query": q,
            "count": len(results),
            "results": results,
        })
