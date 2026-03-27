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
import time

# -------------------------
# Setup browser (NO headless)
# -------------------------
chrome_options = Options()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

wait = WebDriverWait(driver, 15)

cutoff_date = datetime(2026, 3, 31)

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
# Loop pages (adjust if needed)
# -------------------------
for page in range(1, 6):
    url = f"https://morristourism.org/Events?dlv_OC%20CL%20Public%20Events%20Listing=(pageindex={page})"
    print("Scraping page", page)

    driver.get(url)
    time.sleep(3)

    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list-item-container")))
    except:
        print("No events found")
        continue

    events = driver.find_elements(By.CSS_SELECTOR, ".list-item-container")
    print("Events found:", len(events))

    for e in events:
        try:
            title = e.find_element(By.CSS_SELECTOR, "h2.list-item-title").text
            link = e.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            continue

        try:
            desc = e.find_element(By.CSS_SELECTOR, ".list-item-block-desc").text
        except:
            desc = ""

        try:
            location = e.find_element(By.CSS_SELECTOR, ".list-item-address").text
        except:
            location = None

        # -------------------------
        # DATE FILTER LOGIC
        # -------------------------
        keep = False

        try:
            # Example formats:
            # "February 3, 2026 - June 20, 2026"
            # "March 15, 2026"
            first_line = desc.split("\n")[0]

            if " - " in first_line:
                start_str, end_str = first_line.split(" - ")
                end_date = datetime.strptime(end_str.strip(), "%B %d, %Y")

                # keep if event is still ongoing after March 31
                if end_date >= cutoff_date:
                    keep = True
            else:
                event_date = datetime.strptime(first_line.strip(), "%B %d, %Y")
                if event_date >= cutoff_date:
                    keep = True

        except:
            keep = True  # fallback (don’t lose data)

        if not keep:
            continue

        all_new_events.append({
            "name": title,
            "date": desc,
            "location": location,
            "town": None,
            "category": "Community / Tourism",
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