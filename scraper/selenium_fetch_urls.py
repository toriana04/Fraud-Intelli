"""
=====================================================================
 INTELLIFRAUD — SELENIUM URL DISCOVERY (CI-RESILIENT VERSION)
 Handles:
   - Headless Chromium
   - FINRA bot checks
   - Missing search bar
   - Slow page load
=====================================================================
"""

import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SEARCH_QUERY = "fraud"
BASE_URL = "https://www.finra.org"

MAX_LINKS = 60
OUTPUT_JSON = "../data/article_urls.json"

ALLOWED_SOURCES = [
    "https://www.finra.org/media-center/news-releases/",
    "https://www.finra.org/investors/insights/",
    "https://www.finra.org/media-center/",
    "https://www.finra.org/rules-guidance/notices/",
]


def url_allowed(url: str):
    return any(url.startswith(prefix) for prefix in ALLOWED_SOURCES)


def get_driver():
    """Return Chromium driver with realistic user-agent for FINRA."""

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # **Important: Spoof user-agent to avoid bot-block**
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # Use Chromium binary for GitHub Actions
    if os.path.exists("/usr/bin/chromium-browser"):
        options.binary_location = "/usr/bin/chromium-browser"

    return webdriver.Chrome(options=options)


def find_search_box(driver, wait):
    """Tries multiple methods to locate FINRA's search bar (FINRA changes layout often)."""

    selectors = [
        (By.CLASS_NAME, "custom-landing-search"),
        (By.CSS_SELECTOR, "input[type='search']"),
        (By.CSS_SELECTOR, ".search-input"),
        (By.ID, "searchInput"),
    ]

    for method, value in selectors:
        try:
            print(f"[INFO] Trying search selector: {method} → {value}")
            return wait.until(EC.presence_of_element_located((method, value)))
        except:
            pass

    return None


def fetch_urls():
    print("\n[+] Launching Selenium Browser…\n")

    driver = get_driver()
    wait = WebDriverWait(driver, 20)

    driver.get(BASE_URL)
    time.sleep(3)  # Allow JS to load

    print("[+] Searching for FINRA search bar…")

    search_box = find_search_box(driver, wait)

    if search_box is None:
        print("\n[ERROR] Could not find search bar. Printing first 500 chars of page:\n")
        print(driver.page_source[:500])
        driver.quit()
        raise RuntimeError("FINRA search bar not found — CI blocked or layout changed.")

    search_box.send_keys(SEARCH_QUERY)
    search_box.send_keys(Keys.ENTER)

    collected = set()

    while len(collected) < MAX_LINKS:
        time.sleep(2)

        links = driver.find_elements(By.CLASS_NAME, "search-url")

        for l in links:
            url = l.text.strip()
            if url and url_allowed(url):
                collected.add(url)
                print(f"[+] Added URL: {url}")

            if len(collected) >= MAX_LINKS:
                break

        # Try next page
        try:
            next_btn = driver.find_element(By.CLASS_NAME, "enabled")
            driver.execute_script("arguments[0].click();", next_btn)
        except:
            print("[INFO] No more pages.")
            break

    driver.quit()

    os.makedirs("../data", exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(list(collected), f, indent=4)

    print(f"\n✔ Saved {len(collected)} URLs → {OUTPUT_JSON}\n")
    return list(collected)


if __name__ == "__main__":
    fetch_urls()
