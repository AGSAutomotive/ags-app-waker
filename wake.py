import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

STREAMLIT_URL = "https://verneylogyt.streamlit.app/"

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

 # 4. Bulletproof Selector Engine
    print("Scanning page for the strict interactive button element...")
    try:
        # Target the exact clickable button tag directly
        button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.st-emotion-cache-12oz5aa, button"))
        )
        app_is_asleep = True
    except Exception:
        app_is_asleep = False

    # 5. Force-Click Execution Logic
    if app_is_asleep:
        print("Status: App is asleep! 💤 Executing forced click sequence...")
        
        # Use Javascript execution to click it natively. 
        # This completely bypasses layer obstructions or text alignment issues!
        driver.execute_script("arguments[0].click();", button)
        print("Javascript force-click injected successfully. ✅")
        
        # Give Streamlit's back-end a 5-second buffer to lock in the request
        time.sleep(5)
        print("Container initialization request locked in. Rebuilding sequence initiated!")
    else:
        print("Status: No wake button detected within timeout limit.")
        print("Interpretation: App is already fully awake and online! No action needed. ✅")
