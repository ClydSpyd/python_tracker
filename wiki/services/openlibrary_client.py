import requests

OPENLIB_SEARCH = "https://openlibrary.org/search.json"
COVER_BASE = "https://covers.openlibrary.org/b"
WORKS_API = "https://openlibrary.org"

class OpenLibraryError(Exception):
    pass

def build_cover_url(doc: dict) -> str | None:
    cover_i = doc.get("cover_i")
    if isinstance(cover_i, int):
        return f"{COVER_BASE}/id/{cover_i}-M.jpg"
    olid = doc.get("cover_edition_key")
    if isinstance(olid, str):
        return f"{COVER_BASE}/olid/{olid}-M.jpg"
    isbns = doc.get("isbn") or []
    if isinstance(isbns, list) and isbns:
        return f"{COVER_BASE}/isbn/{isbns[0]}-M.jpg"
    return None

def search_books(q: str, limit: int = 20) -> list[dict]:
    fields = ",".join([
        "key","title","author_name","first_publish_year",
        "cover_i","cover_edition_key","edition_key","isbn",
    ])
    try:
        r = requests.get(OPENLIB_SEARCH, params={"q": q, "limit": limit, "fields": fields}, timeout=6)
        r.raise_for_status()
    except requests.RequestException as e:
        raise OpenLibraryError(str(e))

    docs = r.json().get("docs", [])
    out = []
    for d in docs:
        out.append({
            "title": d.get("title"),
            "authors": d.get("author_name") or [],
            "year": d.get("first_publish_year"),
            "cover": build_cover_url(d),
            "work_key": d.get("key"),
            "olid": d.get("cover_edition_key"),
            "edition_key": (d.get("edition_key") or [None])[0],
        })
    return out

def fetch_work_description(work_key: str | None) -> str | None:
    if not work_key:
        return None
    try:
        r = requests.get(f"{WORKS_API}{work_key}.json", timeout=6)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException:
        return None
    desc = data.get("description")
    if isinstance(desc, dict):
        return desc.get("value")
    if isinstance(desc, str):
        return desc
    return None
