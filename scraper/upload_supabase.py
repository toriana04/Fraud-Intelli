"""
=====================================================================
 INTELLIFRAUD — SUPABASE CSV UPLOADER
 Uploads fraud_articles.csv to Supabase Storage.
=====================================================================
"""

import os
from supabase import create_client, Client

CSV_PATH = "../data/fraud_articles.csv"
BUCKET_NAME = "intellifraud"
DESTINATION_FILE = "fraud_articles.csv"


def upload_file():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError("Supabase credentials missing from environment variables.")

    supabase: Client = create_client(url, key)

    with open(CSV_PATH, "rb") as f:
        file_bytes = f.read()

    print("[+] Uploading CSV to Supabase...")
    res = supabase.storage.from_(BUCKET_NAME).upload(
        path=DESTINATION_FILE,
        file=file_bytes,
        file_options={"cacheControl": "3600", "upsert": True}
    )

    print("✔ Upload complete:", res)
    return res


if __name__ == "__main__":
    upload_file()
