import os
import base64
from supabase import create_client, Client

CSV_PATH = "fraud_articles.csv"
BUCKET_NAME = "DTSC_project"

def decode_env(key: str):
    """Decode Base64 secrets safely."""
    value = os.getenv(key)
    if not value:
        return None
    return base64.b64decode(value).decode("utf-8")

# ----------------------------
# Load Base64-encoded secrets
# ----------------------------
SUPABASE_URL = decode_env("SUPABASE_URL_BASE64")
SUPABASE_KEY = decode_env("SUPABASE_KEY_BASE64")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials missing from environment variables.")

# ----------------------------
# Create Supabase client
# ----------------------------
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_file():
    print("[+] Uploading CSV to Supabase...")

    with open(CSV_PATH, "rb") as f:
        data = f.read()

    # Upload/replace CSV in the bucket
    result = supabase.storage.from_(BUCKET_NAME).upload(
        path=CSV_PATH,
        file=data,
        file_options={"content-type": "text/csv", "upsert": True}
    )

    print("[✓] Upload successful!")
    print("Supabase response:", result)

if __name__ == "__main__":
    upload_file()
