import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 1. Target URL Setup (Currently pointed to a known sleeping app for your test)
# Swap this back to "https://agsroofmappingtool.streamlit.app/" when your test passes!
STREAMLIT_URL = os.environ.get("https://verneylogyt.streamlit.app/")

print(f"Launching headless browser to inspect: {STREAMLIT_URL}")

# 2. Configure Headless Chrome Options for GitHub Actions
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# 3. Initialize the Driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(STREAMLIT_URL)
    print("Page opened. Analyzing DOM structure and waiting for state elements...")

    # Punctuation-immune XPath targeting the core text inside sleepinactivity.png
    wake_button_xpath = "//button[contains(text(), 'app back up')]"

    # 4. Dynamic Verification Engine
    print("Scanning page for the Streamlit sleep container...")
    try:
        # Actively poll the DOM for up to 25 seconds for the sleep button
        button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.XPATH, wake_button_xpath))
        )
        app_is_asleep = True
    except Exception:
        # If the button doesn't appear within 25 seconds, assume the app is already live
        app_is_asleep = False

    # 5. Execution Logic
    if app_is_asleep:
        print("Status: App is asleep! 💤 Attempting to wake it up...")
        button.click()
        
        # Verify that the button disappears, confirming the container began its rebuild cycle
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, wake_button_xpath)))
        print("Button clicked successfully! App container is rebuilding. ✅")
    else:
        print("Status: No wake button detected within timeout limit.")
        print("Interpretation: App is already fully awake and online! No action needed. ✅")

except Exception as e:
    print(f"An unexpected tracking error occurred during automation: {e}")
    # Fallback safety capture
    try:
        driver.save_screenshot("error_screenshot.png")
        print("Saved 'error_screenshot.png' due to compilation error.")
    except Exception as screenshot_error:
        print(f"Could not capture screenshot: {screenshot_error}")
finally:
    driver.quit()
    print("Session securely closed.")
