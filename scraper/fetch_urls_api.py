"""
=====================================================================
 INTELLIFRAUD — FINRA SEARCH API SCRAPER
 Stable, browserless, CI/CD safe. Replaces Selenium entirely.
=====================================================================
"""

import os
import json
import requests

OUTPUT_JSON = "../data/article_urls.json"
QUERY = "fraud"
MAX_RESULTS = 200  # Adjust for more/less results


def fetch_urls_api():
    print("\n[+] Fetching FINRA URLs via Search API…\n")

    api_url = (
        "https://www.finra.org/search-api/search-all"
        f"?query={QUERY}&offset=0&limit={MAX_RESULTS}"
    )

    response = requests.get(api_url, timeout=20)

    if response.status_code != 200:
        raise RuntimeError(
            f"FINRA API request failed with status {response.status_code}"
        )

    data = response.json()
    urls = set()

    for item in data.get("results", []):
        url = item.get("url")
        if url and url.startswith("http"):
            urls.add(url)

    os.makedirs("../data", exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(list(urls), f, indent=4)

    print(f"\n✔ Retrieved {len(urls)} URLs → {OUTPUT_JSON}\n")
    return list(urls)


if __name__ == "__main__":
    fetch_urls_api()
