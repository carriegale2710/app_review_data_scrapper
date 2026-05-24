import re
from urllib.parse import urlparse, parse_qs
import pandas as pd
from google_play_scraper import reviews, Sort
from app_store_web_scraper import AppStoreEntry


GOOGLE_PLAY_URL = "https://play.google.com/store/apps/details?id=com.spotify.music"
APPLE_APP_STORE_URL = "https://apps.apple.com/us/app/spotify-music-and-podcasts/id324684580"

COUNTRY = "us"
LANG = "en"
PLAY_LIMIT = 500
APP_STORE_LIMIT = 500
OUTPUT_FILE = "combined_app_reviews.csv"


def extract_google_play_id(url: str) -> str:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    app_id = query.get("id", [None])[0]
    if not app_id:
        raise ValueError("Could not find Google Play package name in URL.")
    return app_id


def extract_apple_app_id(url: str) -> int:
    match = re.search(r"/id(\d+)", url)
    if not match:
        raise ValueError("Could not find Apple numeric app ID in URL.")
    return int(match.group(1))


def fetch_google_play_reviews(app_id, country="us", lang="en", limit=500):
    rows = []
    token = None

    while len(rows) < limit:
        batch_size = min(200, limit - len(rows))
        batch, token = reviews(
            app_id,
            lang=lang,
            country=country,
            sort=Sort.NEWEST,
            count=batch_size,
            continuation_token=token
        )

        if not batch:
            break

        for r in batch:
            rows.append({
                "store": "google_play",
                "app_id": app_id,
                "review_id": r.get("reviewId"),
                "date": r.get("at"),
                "rating": r.get("score"),
                "title": None,
                "text": r.get("content"),
                "user_name": r.get("userName"),
                "developer_reply": r.get("replyContent"),
                "developer_reply_date": r.get("repliedAt"),
                "version": r.get("reviewCreatedVersion"),
                "thumbs_up": r.get("thumbsUpCount"),
                "country": country,
                "language": lang
            })

        if token is None:
            break

    return pd.DataFrame(rows)


def fetch_app_store_reviews(app_id, country="us", limit=500):
    app = AppStoreEntry(app_id=app_id, country=country)
    rows = []

    for i, review in enumerate(app.reviews()):
        if i >= limit:
            break

        rows.append({
            "store": "app_store",
            "app_id": app_id,
            "review_id": getattr(review, "id", None),
            "date": getattr(review, "date", None),
            "rating": getattr(review, "rating", None),
            "title": getattr(review, "title", None),
            "text": getattr(review, "review", None) or getattr(review, "content", None),
            "user_name": getattr(review, "user_name", None),
            "developer_reply": getattr(review, "developer_response", None),
            "developer_reply_date": getattr(review, "developer_response_date", None),
            "version": getattr(review, "app_version", None),
            "thumbs_up": None,
            "country": country,
            "language": None
        })

    return pd.DataFrame(rows)


play_app_id = extract_google_play_id(GOOGLE_PLAY_URL)
apple_app_id = extract_apple_app_id(APPLE_APP_STORE_URL)

gp_df = fetch_google_play_reviews(
    app_id=play_app_id,
    country=COUNTRY,
    lang=LANG,
    limit=PLAY_LIMIT
)

as_df = fetch_app_store_reviews(
    app_id=apple_app_id,
    country=COUNTRY,
    limit=APP_STORE_LIMIT
)

combined = pd.concat([gp_df, as_df], ignore_index=True)
combined["date"] = pd.to_datetime(combined["date"], errors="coerce")
combined = combined.sort_values(["date", "store"], ascending=[False, True])

combined.to_csv(OUTPUT_FILE, index=False)

print(f"Saved {len(combined)} rows to {OUTPUT_FILE}")
print(combined.head(10))