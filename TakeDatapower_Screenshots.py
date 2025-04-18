from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Initialize the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print("Navigating to DataPower WebUI...")
    driver.get("https://localhost:9090")
    
    # Handle security warning
    try:
        print("Checking for security warning...")
        advance_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "details-button"))
        )
        advance_button.click()
        
        proceed_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "proceed-link"))
        )
        proceed_link.click()
        print("Bypassed security warning")
    except Exception:
        print("No security warning detected")
    
    # Wait for login page
    print("Waiting for login page...")
    username_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "idx_form_TextBox_0"))
    )
    
    # Login process
    print("Logging in...")
    username_field.clear()
    username_field.send_keys("admin")
    
    password_field = driver.find_element(By.ID, "dpLoginFramePassword")
    password_field.clear()
    password_field.send_keys("admin")
    
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "dijit_form_Button_0"))
    )
    login_button.click()
    
    print("Waiting for dashboard to load...")
    time.sleep(5)  # Wait for the page to load completely
    
    # Locate the search bar, enter 'Web Service Proxy', and press Enter
    print("Searching for Web Service Proxy...")
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
    )
    search_bar.clear()
    search_bar.send_keys("Web Service Proxy")
    search_bar.send_keys(Keys.RETURN)
    
    print("Search executed. Waiting for results...")
    time.sleep(5)  # Allow time for search results to appear
    
    # Click on the 3rd result from the search list
    print("Clicking on the third Web Service Proxy result...")
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), 'Web Service Proxy')]")
    ))
    
    if len(results) >= 3:
        results[2].click()
        print("Clicked on the third Web Service Proxy result.")
    else:
        print("Less than three results found, unable to click the third one.")
    
    # Take a screenshot for debugging
    screenshot_path = "Datapower_WebserviceProxy_Screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")
    
    # Wait longer before closing the browser
    print("Pausing before closing the browser...")
    time.sleep(10)
    
except Exception as e:
    print(f"An error occurred: {str(e)}")
    
finally:
    print("Closing browser...")
    driver.quit()
