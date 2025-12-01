# =====================================================================
#             INTELLIFRAUD — SELENIUM URL DISCOVERY (CI SAFE)
#  Works locally AND on GitHub Actions (headless, Chrome binary set)
# =====================================================================

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

def url_allowed(url):
    return any(url.startswith(prefix) for prefix in ALLOWED_SOURCES)

def get_driver():
    """Create a Chrome WebDriver instance that works on GitHub Actions + locally."""
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # For GitHub Actions: Chrome is installed at this path
    if os.path.exists("/usr/bin/google-chrome"):
        options.binary_location = "/usr/bin/google-chrome"

    # Create driver
    driver = webdriver.Chrome(options=options)
    return driver

def fetch_urls():
    print("\n[+] Launching Selenium Browser…\n")

    driver = get_driver()
    wait = WebDriverWait(driver, 10)

    driver.get(BASE_URL)

    # Search bar
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

        # pagination
        try:
            next_btn = driver.find_element(By.CLASS_NAME, "enabled")
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(1)
        except:
            print("\n[INFO] No more pages.\n")
            break

    driver.quit()

    # Save to JSON
    os.makedirs("../data", exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(list(collected), f, indent=4)

    print(f"\n✔ Saved {len(collected)} URLs → {OUTPUT_JSON}\n")
    return list(collected)

if __name__ == "__main__":
    fetch_urls()
