"""
=====================================================================
 INTELLIFRAUD — SUPABASE CSV UPLOADER (FINAL VERSION)
 Bucket: DTSC_project
=====================================================================
"""

import os
from supabase import create_client, Client

CSV_PATH = "../data/fraud_articles.csv"
BUCKET_NAME = "DTSC_project"   # <-- FIXED BUCKET NAME
DESTINATION_FILE = "fraud_articles.csv"


def upload_file():
    url = os.getenv("https://debqilwldhawthyjrlsh.supabase.co")
    key = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlYnFpbHdsZGhhd3RoeWpybHNoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NDE4ODMsImV4cCI6MjA3NjIxNzg4M30.gsTqH9cQKjqOR6SZ81jN82DV4hMLTynjdDmvNrfH5uE")

    if not url or not key:
        raise RuntimeError("Supabase credentials missing from environment variables.")

    supabase: Client = create_client(url, key)

    print("\n[+] Uploading CSV to Supabase (using update)…\n")

    with open(CSV_PATH, "rb") as f:
        file_bytes = f.read()

    # Use update() because upload() requires upsert headers that break in GitHub Actions
    result = supabase.storage.from_(BUCKET_NAME).update(
        path=DESTINATION_FILE,
        file=file_bytes,
        file_options={
            "contentType": "text/csv",
            "cacheControl": "3600"
        }
    )

    print("✔ Upload complete:", result)
    return result


if __name__ == "__main__":
    upload_file()
