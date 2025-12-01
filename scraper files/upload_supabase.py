# =====================================================================
#                    INTELLIFRAUD — SUPABASE UPLOADER
# =====================================================================

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("https://debqilwldhawthyjrlsh.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlYnFpbHdsZGhhd3RoeWpybHNoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NDE4ODMsImV4cCI6MjA3NjIxNzg4M30.gsTqH9cQKjqOR6SZ81jN82DV4hMLTynjdDmvNrfH5uE")
SUPABASE_BUCKET = "DTSC_project"

LOCAL_FILE = "../data/fraud_articles.csv"
REMOTE_PATH = "csv/fraud_articles.csv"  # Streamlit will read this

def upload():
    sb = create_client(SUPABASE_URL, SUPABASE_KEY)

    with open(LOCAL_FILE, "rb") as f:
        sb.storage.from_(SUPABASE_BUCKET).upload(
            REMOTE_PATH,
            f,
            file_options={"content-type": "text/csv", "upsert": "true"}
        )

    print("✔ Uploaded fraud_articles.csv to Supabase")

if __name__ == "__main__":
    upload()
