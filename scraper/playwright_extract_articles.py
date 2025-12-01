"""
=====================================================================
 INTELLIFRAUD — PLAYWRIGHT ARTICLE SCRAPER
 Extracts FINRA article metadata + content
=====================================================================
"""

import json
import time
import os
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

INPUT_JSON = "../data/article_urls.json"
OUTPUT_CSV = "../data/fraud_articles.csv"


def extract_article(playwright, url):
    """Extract title, date, and body from FINRA article pages."""

    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, timeout=60000)

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    browser.close()

    # Extract fields
    title = soup.find("h1")
    title = title.text.strip() if title else "No Title"

    date = soup.find("time")
    date = date.text.strip() if date else "No Date"

    # body text
    paragraphs = soup.find_all("p")
    body = "\n".join([p.text.strip() for p in paragraphs])

    return {
        "url": url,
        "title": title,
        "date": date,
        "body": body,
    }


def run_playwright():
    """Runs Playwright article extraction for each URL."""

    if not os.path.exists(INPUT_JSON):
        raise FileNotFoundError(f"{INPUT_JSON} not found")

    with open(INPUT_JSON, "r") as f:
        urls = json.load(f)

    print(f"[+] Loaded {len(urls)} URLs from {INPUT_JSON}")

    data = []

    with sync_playwright() as p:
        for url in urls:
            try:
                print(f"[+] Extracting: {url}")
                article_data = extract_article(p, url)
                data.append(article_data)
            except Exception as e:
                print(f"[ERROR] Could not extract {url}: {e}")

    df = pd.DataFrame(data)

    os.makedirs("../data", exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"\n✔ Saved {len(df)} articles → {OUTPUT_CSV}\n")


if __name__ == "__main__":
    run_playwright()
