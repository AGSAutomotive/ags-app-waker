import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

STREAMLIT_URL = os.environ.get("STREAMLIT_APP_URL", "https://verneylogyt.streamlit.app/")

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
    print("Page opened. Waiting for elements to load...")
    time.sleep(10)

    wake_button_xpath = "//*[contains(text(), 'Yes, get this app back up!')]"

    if len(driver.find_elements(By.XPATH, wake_button_xpath)) > 0:
        print("Status: App is asleep! 💤 Attempting to wake it up...")
        button = driver.find_element(By.XPATH, wake_button_xpath)
        button.click()

        wait = WebDriverWait(driver, 20)
        wait.until(EC.invisibility_of_element_located((By.XPATH, wake_button_xpath)))
        print("Button clicked successfully! App container is rebuilding. ✅")
    else:
        print("Status: App is already fully awake and online! No action needed. ✅")

except Exception as e:
    print(f"An unexpected tracking error occurred: {e}")
    driver.save_screenshot("error_screenshot.png")
finally:
    driver.quit()
    print("Session closed.")
