from playwright.sync_api import sync_playwright
import smtplib
from email.message import EmailMessage
import os
from datetime import datetime
import re

# =====================================
# CONFIGURATION
# =====================================

URL = "https://ai.icai.org/aica_level2.php"

TARGET_LOCATIONS = [
    "Delhi",
    "Gurgaon",
    "Gurugram",
    "Faridabad",
    
]

EMAIL = "YOUR_GMAIL@gmail.com"

PASSWORD = "YOUR_APP_PASSWORD"

DATE_FILE = "last_email_date.txt"


# =====================================
# EMAIL FUNCTION
# =====================================

def send_email(available_locations):

    msg = EmailMessage()

    msg['Subject'] = 'ICAI Slot Availability Alert'

    msg['From'] = EMAIL

    msg['To'] = EMAIL

    body = "ICAI AI Course Slots Available\n\n"

    for location, seats in available_locations:

        body += f"Location: {location}\n"
        body += f"Available Seats: {seats}\n\n"

    body += "Website:\nhttps://ai.icai.org/aica_level2.php"

    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(EMAIL, PASSWORD)

        smtp.send_message(msg)

        print("📧 Consolidated Email Alert Sent!")


# =====================================
# DAILY EMAIL CONTROL
# =====================================

today = datetime.now().strftime("%Y-%m-%d")

email_already_sent_today = False

if os.path.exists(DATE_FILE):

    with open(DATE_FILE, "r") as file:

        saved_date = file.read().strip()

        if saved_date == today:

            email_already_sent_today = True


# =====================================
# MAIN AUTOMATION
# =====================================

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(URL)

    page.wait_for_selector("text=Batch")

    links = page.locator("a")

    count = links.count()

    found = False

    available_locations = []

    checked_links = []

    for i in range(count):

        try:

            text = links.nth(i).inner_text()

            href = links.nth(i).get_attribute("href")

            if text and href:

                for location in TARGET_LOCATIONS:

                    if location.upper() in text.upper():

                        full_link = "https://ai.icai.org/" + href

                        if full_link not in checked_links:

                            checked_links.append(full_link)

                            detail_page = browser.new_page()

                            detail_page.goto(full_link)

                            detail_page.wait_for_load_state("networkidle")

                            detail_page.wait_for_timeout(3000)

                            detail_text = detail_page.locator("body").inner_text()

                            match = re.search(
                                r'Available Seat:\s*(\d+)',
                                detail_text
                            )

                            if match:

                                seats = int(match.group(1))

                                if seats > 0:

                                    found = True

                                    print(f"\n✅ SLOT AVAILABLE IN {location}")

                                    print(f"Available Seats: {seats}")

                                    available_locations.append((location, seats))

                            detail_page.close()

        except:
            pass

    # SEND ONLY ONE EMAIL
    if found and not email_already_sent_today:

        send_email(available_locations)

        with open(DATE_FILE, "w") as file:

            file.write(today)

    if not found:

        print("\n❌ No slots available in preferred locations")

    browser.close()