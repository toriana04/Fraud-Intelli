"""
=====================================================================
 INTELLIFRAUD — SELENIUM URL DISCOVERY (CI-SAFE VERSION)
 Works in GitHub Actions (Chromium + Headless)
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
    """Return a Chromium-based driver that works locally and on GitHub Actions."""

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # GitHub Actions uses Chromium installed at this location
    if os.path.exists("/usr/bin/chromium-browser"):
        options.binary_location = "/usr/bin/chromium-browser"

    return webdriver.Chrome(options=options)


def fetch_urls():
    print("\n[+] Launching Selenium Browser…\n")

    driver = get_driver()
    wait = WebDriverWait(driver, 10)

    driver.get(BASE_URL)

    print("[+] Searching FINRA…")
    search_box = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "custom-landing-search"))
    )
    search_box.send_keys(SEARCH_QUERY)
    search_box.send_keys(Keys.ENTER)

    collected = set()

    while len(collected) < MAX_LINKS:
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "search-url")))
        links = driver.find_elements(By.CLASS_NAME, "search-url")

        for l in links:
            url = l.text.strip()
            if url and url_allowed(url):
                collected.add(url)
                print(f"[+] Added URL: {url}")

            if len(collected) >= MAX_LINKS:
                break

        # Try pagination
        try:
            next_btn = driver.find_element(By.CLASS_NAME, "enabled")
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(1)
        except:
            print("\n[INFO] No more pages available.\n")
            break

    driver.quit()

    # Save results
    os.makedirs("../data", exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(list(collected), f, indent=4)

    print(f"\n✔ Saved {len(collected)} URLs → {OUTPUT_JSON}\n")
    return list(collected)


if __name__ == "__main__":
    fetch_urls()
