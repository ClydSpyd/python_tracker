import requests
from django.conf import settings

class OmdbError(Exception):
    pass

def fetch_by_imdb_id(imdb_id: str) -> dict:
    api_key = getattr(settings, "OMDB_API_KEY", None)
    if not api_key:
        raise OmdbError("OMDB_API_KEY not set in settings.")

    try:
        r = requests.get(
            "http://www.omdbapi.com/",
            params={"apikey": api_key, "i": imdb_id, "plot": "full"},
            timeout=6,
        )
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        raise OmdbError(f"OMDb unreachable: {e}")

    if data.get("Response") == "False":
        raise OmdbError(data.get("Error") or "Movie not found")

    return data


def map_omdb_payload(omdb: dict, imdb_id: str) -> dict:
    def to_int(s):
        try:
            return int(str(s).replace(',', '').split()[0])
        except Exception:
            return None

    return {
        "imdb_id": imdb_id,
        "title": omdb.get("Title"),
        "year": to_int(omdb.get("Year", "")),
        "released": omdb.get("Released"),
        "runtime": to_int(omdb.get("Runtime") or ""),
        "genre": omdb.get("Genre"),
        "director": omdb.get("Director"),
        "actors": omdb.get("Actors"),
        "plot": omdb.get("Plot"),
        "language": omdb.get("Language"),
        "poster_url": omdb.get("Poster"),
        "metascore": to_int(omdb.get("Metascore")),
        "ratings": omdb.get("Ratings", []),
        "imdb_rating": (float(omdb["imdbRating"]) if omdb.get("imdbRating") not in (None, "N/A") else None),
        "imdb_votes": to_int(omdb.get("imdbVotes")),
    }
