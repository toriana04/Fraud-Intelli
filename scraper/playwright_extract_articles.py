# =====================================================================
#            INTELLIFRAUD — PLAYWRIGHT ARTICLE EXTRACTION
#    Extracts Title, Date, Summary, Keywords from FINRA Articles
# =====================================================================

import json
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from keybert import KeyBERT
from transformers import pipeline
import spacy
import os

URL_JSON = "../data/article_urls.json"
OUTPUT_CSV = "../data/fraud_articles.csv"

# NLP Models
nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def clean_text(text):
    doc = nlp(text)
    return " ".join([t.text.lower() for t in doc if t.is_alpha and not t.is_stop])

def extract_date(page):
    # Try <time> element
    try:
        t = page.locator("time").first.inner_text().strip()
        if t:
            return t
    except:
        pass

    # Try metadata
    metas = page.locator("meta").all()
    for m in metas:
        try:
            prop = m.get_attribute("property")
            if prop and "published" in prop.lower():
                return m.get_attribute("content")
        except:
            pass

    return "Unknown"

def main():
    with open(URL_JSON, "r") as f:
        urls = json.load(f)

    rows = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i, url in enumerate(urls):
            print(f"[{i+1}/{len(urls)}] Scraping: {url}")

            try:
                page.goto(url, wait_until="networkidle")

                html = page.content()
                soup = BeautifulSoup(html, "html.parser")

                # Extract title
                title_tag = soup.find("h1")
                title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"

                # Extract publication date
                pub_date = extract_date(page)

                # Extract article body
                body = soup.find("div", class_="block-region-middle")
                body_text = body.get_text(" ", strip=True) if body else soup.get_text(" ", strip=True)

                # Generate summary
                try:
                    summary = summarizer(body_text[:3000], max_length=140, min_length=40)[0]["summary_text"]
                except:
                    summary = body_text[:200]

                # Keywords
                cleaned = clean_text(body_text)
                try:
                    kws = kw_model.extract_keywords(cleaned, top_n=10)
                    keywords = ", ".join([kw for kw, _ in kws])
                except:
                    keywords = ""

                rows.append({
                    "url": url,
                    "title": title,
                    "date": pub_date,
                    "summary": summary,
                    "keywords": keywords
                })

            except Exception as e:
                print(f"[ERROR] Failed to extract: {url} — {e}")
                continue

        browser.close()

    os.makedirs("../data", exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"\n✔ Extraction complete → {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
