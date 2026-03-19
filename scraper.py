from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import os
from datetime import datetime

# -------------------------
# Setup browser (NO headless)
# -------------------------
chrome_options = Options()
# DO NOT use headless here

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

wait = WebDriverWait(driver, 15)

cutoff_date = datetime(2026, 3, 18)

# -------------------------
# Load existing JSON
# -------------------------
if os.path.exists("data.json"):
    with open("data.json", "r") as f:
        existing_events = json.load(f)
else:
    existing_events = []

all_new_events = []

# -------------------------
# Loop pages 1–8
# -------------------------
for page in range(1, 9):
    url = f"https://www.mclib.info/Events?dlv_OC%20CL%20Public%20Events%20Listing=(pageindex={page})"
    print("Scraping page", page)

    driver.get(url)

    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list-item-container")))
    except:
        print("Events did not load")
        continue

    events = driver.find_elements(By.CSS_SELECTOR, ".list-item-container")
    print("Events found:", len(events))

    for e in events:
        try:
            title = e.find_element(By.CSS_SELECTOR, "h2.list-item-title").text
        except:
            continue

        try:
            link = e.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            link = None

        try:
            date_text = e.find_element(By.CSS_SELECTOR, ".list-item-block-desc").text
        except:
            continue

        try:
            location = e.find_element(By.CSS_SELECTOR, ".list-item-address").text
        except:
            location = "Morris County Library"

        # -------------------------
        # FILTER DATE
        # -------------------------
        try:
            first_line = date_text.split("\n")[0]
            parsed_date = datetime.strptime(first_line.split(" - ")[0], "%B %d, %Y")
            if parsed_date < cutoff_date:
                continue
        except:
            pass

        all_new_events.append({
            "name": title,
            "date": date_text,
            "location": location,
            "town": "Morris County",
            "category": "Library / Community",
            "url": link,
            "latitude": None,
            "longitude": None
        })

driver.quit()

# -------------------------
# Merge + dedupe
# -------------------------
combined = existing_events + all_new_events

unique_events = []
seen = set()

for event in combined:
    key = (event.get("name"), event.get("date"))
    if key not in seen:
        seen.add(key)
        unique_events.append(event)

with open("data.json", "w") as f:
    json.dump(unique_events, f, indent=2)

print("✅ DONE! Total events:", len(unique_events))