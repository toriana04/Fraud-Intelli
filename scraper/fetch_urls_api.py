"""
=====================================================================
INTELLIFRAUD — FINRA BACKEND SEARCH API SCRAPER (UNBLOCKABLE VERSION)
Uses the REAL internal FINRA API endpoint + proper headers.
=====================================================================
"""

import os
import json
import requests

OUTPUT_JSON = "../data/article_urls.json"
QUERY = "fraud"
MAX_PAGES = 5  # Fetch more pages if needed (each page has ~10 results)

FINRA_API = "https://www.finra.org/api/search/all"


def fetch_urls_api():
    print("\n[+] Fetching FINRA URLs via backend API…\n")

    urls = set()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.finra.org/",
    }

    for page in range(1, MAX_PAGES + 1):
        params = {"query": QUERY, "page": page}

        r = requests.get(FINRA_API, headers=headers, params=params, timeout=20)

        if r.status_code != 200:
            print(f"[WARN] Page {page} failed with status {r.status_code}")
            continue

        data = r.json()

        results = data.get("results", [])
        if not results:
            break  # No more pages

        for item in results:
            url = item.get("url")
            if url and url.startswith("http"):
                urls.add(url)

    # Save results
    os.makedirs("../data", exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(list(urls), f, indent=4)

    print(f"\n✔ Retrieved {len(urls)} URLs → {OUTPUT_JSON}\n")
    return list(urls)


if __name__ == "__main__":
    fetch_urls_api()
