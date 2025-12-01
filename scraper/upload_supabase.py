"""
=====================================================================
 INTELLIFRAUD — SUPABASE CSV UPLOADER
 Uploads fraud_articles.csv to Supabase Storage
=====================================================================
"""

import os
from supabase import create_client, Client

CSV_PATH = "../data/fraud_articles.csv"
BUCKET_NAME = "intellifraud"
DESTINATION = "fraud_articles.csv"


def upload_file():
    url = os.getenv("https://debqilwldhawthyjrlsh.supabase.co")
    key = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlYnFpbHdsZGhhd3RoeWpybHNoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NDE4ODMsImV4cCI6MjA3NjIxNzg4M30.gsTqH9cQKjqOR6SZ81jN82DV4hMLTynjdDmvNrfH5uE")

    if not url or not key:
        raise ValueError("Missing Supabase credentials in environment variables.")

    supabase: Client = create_client(url, key)

    # Read file bytes
    with open(CSV_PATH, "rb") as f:
        data = f.read()

    print("[+] Uploading CSV to Supabase...")
    result = supabase.storage.from_(BUCKET_NAME).upload(DESTINATION, data, upsert=True)

    print("✔ Upload complete:", result)
    return result


if __name__ == "__main__":
    upload_file()
