import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Hardcoded test URL to bypass any GitHub environment variable overrides
STREAMLIT_URL = "https://agsroofmappingtool.streamlit.app/"

print(f"Launching headless browser to inspect: {STREAMLIT_URL}")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(STREAMLIT_URL)
    print("Page opened. Searching for the Streamlit sleep container...")

    # Punctuation-immune XPath targeting the core text inside sleepinactivity.png
    wake_button_xpath = "//button[contains(text(), 'app back up')]"
    
    app_is_asleep = False
    button = None

    try:
        # Actively poll the DOM for up to 25 seconds for the sleep button
        button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.XPATH, wake_button_xpath))
        )
        app_is_asleep = True
    except Exception:
        print("Timeout reached or button not found via text XPath.")

    # If the text check failed, try finding it by the structural button tag as a fallback
    if not app_is_asleep:
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.st-emotion-cache-12oz5aa, button"))
            )
            app_is_asleep = True
        except Exception:
            pass

    # Execution Sequence
    if app_is_asleep and button:
        print("Status: App is asleep! 💤 Injecting native Javascript click sequence...")
        
        # Force a native browser-level click to guarantee execution
        driver.execute_script("arguments[0].click();", button)
        print("Javascript click injected successfully. ✅")
        
        time.sleep(5)
        print("Container initialization sequence successfully initiated!")
    else:
        print("Status: No wake button detected via text or CSS selectors.")
        print("Interpretation: App is already fully awake and online! No action needed. ✅")

except Exception as e:
    print(f"An unexpected tracking error occurred during automation: {e}")
    try:
        driver.save_screenshot("error_screenshot.png")
    except Exception:
        pass
finally:
    driver.quit()
    print("Session securely closed.")
