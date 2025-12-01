"""
=====================================================================
 INTELLIFRAUD — SUPABASE CSV UPLOADER (FIXED FOR NEW SDK)
 Uses update() instead of upload() to avoid header-value errors.
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

    print("[+] Uploading CSV to Supabase (using update)…")

    res = supabase.storage.from_(BUCKET_NAME).update(
        path=DESTINATION_FILE,
        file=file_bytes,
        file_options={"contentType": "text/csv", "cacheControl": "3600"}
    )

    print("✔ Upload complete:", res)
    return res


if __name__ == "__main__":
    upload_file()
