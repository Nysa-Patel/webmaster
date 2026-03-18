from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os

# -------------------------
# Setup Chrome options
# -------------------------
chrome_options = Options()
chrome_options.add_argument("--headless")  # run in background
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# -------------------------
# Setup WebDriver
# -------------------------
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# -------------------------
# Prepare existing data
# -------------------------
if os.path.exists("data.json"):
    with open("data.json", "r") as f:
        existing_events = json.load(f)
else:
    existing_events = []

all_new_events = []

# -------------------------
# Loop through pages
# -------------------------
for page in range(1, 37):  # 36 pages
    url = f"https://www.morriscountynj.gov/Morris-County-Events?dlv_OC%20CL%20Public%20Events%20Listing=(pageindex={page})"
    print(f"Scraping page {page}...")
    driver.get(url)
    time.sleep(3)  # wait for page to load

    # Find all event containers
    events = driver.find_elements(By.CSS_SELECTOR, "div.list-item-container")
    if not events:
        print("No events found on this page, stopping.")
        break

    for e in events:
        try:
            title = e.find_element(By.CSS_SELECTOR, "h2.list-item-title").text
        except:
            title = None

        try:
            link = e.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            link = None

        try:
            date_range = e.find_element(By.CSS_SELECTOR, "span.list-item-block-desc").text
        except:
            date_range = None

        try:
            location = e.find_element(By.CSS_SELECTOR, "p.list-item-address").text
        except:
            location = None

        try:
            tags = e.find_element(By.CSS_SELECTOR, "p.tagged-as-list .text").text
        except:
            tags = None

        all_new_events.append({
            "name": title,
            "date": date_range,
            "location": location,
            "town": None,  # fill manually if desired
            "category": tags if tags else "Community / Family Friendly",
            "url": link,
            "latitude": None,
            "longitude": None
        })

# -------------------------
# Close browser
# -------------------------
driver.quit()

# -------------------------
# Merge with existing data.json
# -------------------------
combined = existing_events + all_new_events

# Remove duplicates based on name + date
unique_events = []
seen = set()
for event in combined:
    key = (event.get("name"), event.get("date"))
    if key not in seen:
        seen.add(key)
        unique_events.append(event)

# Save merged data
with open("data.json", "w") as f:
    json.dump(unique_events, f, indent=2)

print(f"✅ Scraping complete! Total events now in data.json: {len(unique_events)}")