import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .serializers import MovieSerializer
from .models import Movie
from rest_framework.permissions import IsAuthenticated
from users.authentication import CookieJWTAuthentication

OMDB_API_KEY = '9d4b151c'
# OMDB_API_KEY = os.environ.get("OMDB_API_KEY")  # set in your .env or system env
OFFLINE_CACHE = {
    "shining": [
        {
            "Title": "The Shining",
            "Year": "1980",
            "imdbID": "tt0081505",
            "Type": "movie",
            "Poster": "https://m.media-amazon.com/images/M/MV5BNmM5ZThhY2ItOGRjOS00NzZiLWEwYTItNDgyMjFkOTgxMmRiXkEyXkFqcGc@._V1_SX300.jpg"
        },
        {
            "Title": "Shining Through",
            "Year": "1992",
            "imdbID": "tt0105391",
            "Type": "movie",
            "Poster": "https://m.media-amazon.com/images/M/MV5BOGQxZjBhZWEtMmNiYy00Y2M2LWIwNTctZmQyNWNmZTU1YTk5XkEyXkFqcGc@._V1_SX300.jpg"
        },
        {
            "Title": "Making 'The Shining'",
            "Year": "1980",
            "imdbID": "tt0203667",
            "Type": "movie",
            "Poster": "https://m.media-amazon.com/images/M/MV5BMTIyNzNhNTktMDRlOS00ZGE3LThhOTktMDg3YWRkY2EyYTMyXkEyXkFqcGdeQXVyNDk0MDg4NDk@._V1_SX300.jpg"
        },
        {
            "Title": "A Bright Shining Lie",
            "Year": "1998",
            "imdbID": "tt0126220",
            "Type": "movie",
            "Poster": "https://m.media-amazon.com/images/M/MV5BMTQwMTE5MTk4Ml5BMl5BanBnXkFtZTcwMTI0MzAyMQ@@._V1_SX300.jpg"
        },
        {
            "Title": "The Shining Hour",
            "Year": "1938",
            "imdbID": "tt0030743",
            "Type": "movie",
            "Poster": "https://m.media-amazon.com/images/M/MV5BOTU3OWJkMGUtMTU0Ny00NDY4LWE4NzAtNjVhYjg5MjFlZGIxXkEyXkFqcGdeQXVyNjc0MzMzNjA@._V1_SX300.jpg"
        },
        {
            "Title": "Shining Victory",
            "Year": "1941",
            "imdbID": "tt0034184",
            "Type": "movie",
            "Poster": "https://m.media-amazon.com/images/M/MV5BNzg5OTIwMWUtNDQyMi00Y2QzLTg4YWYtY2M4YmYyN2EyNjNhXkEyXkFqcGc@._V1_SX300.jpg"
        },
        {
            "Title": "Our Shining Days",
            "Year": "2017",
            "imdbID": "tt7013194",
            "Type": "movie",
            "Poster": "https://m.media-amazon.com/images/M/MV5BZTM4ZTIyYTQtOGZkNi00NmM2LWFiMjktN2NkZjk0NjFiZGNmXkEyXkFqcGc@._V1_SX300.jpg"
        },
        {
            "Title": "Shining Sex",
            "Year": "1976",
            "imdbID": "tt0232633",
            "Type": "movie",
            "Poster": "https://m.media-amazon.com/images/M/MV5BZjZjMTBkYmYtYThjMy00Mjk1LTk3YmItZTA2ZTgzYWQxNGZiXkEyXkFqcGc@._V1_SX300.jpg"
        },
        {
            "Title": "One Bright Shining Moment",
            "Year": "2005",
            "imdbID": "tt0468528",
            "Type": "movie",
            "Poster": "https://m.media-amazon.com/images/M/MV5BMTM3Mzc4NzkwNF5BMl5BanBnXkFtZTcwOTQxNzIzMQ@@._V1_SX300.jpg"
        },
        {
            "Title": "The Shining in 30 Seconds (and Re-enacted by Bunnies)",
            "Year": "2004",
            "imdbID": "tt0473394",
            "Type": "movie",
            "Poster": "N/A"
        }
    ]
}

class MovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return Movie.objects.filter(user=self.request.user).order_by('title')

class MovieCreateView(generics.CreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

    # If no results, return empty list
    if "Response" in data and data["Response"] == "False":
        return JsonResponse({"Search": []}, safe=False)

    return JsonResponse(data, safe=False)
