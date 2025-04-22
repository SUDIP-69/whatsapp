import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException

# Persistent browser session configuration
USER_DATA_DIR = '/tmp/chrome_profile'  # Persistent storage for browser session
WHATSAPP_URL = 'https://web.whatsapp.com/send?phone={phone}&text={text}'

def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={USER_DATA_DIR}')
    options.add_argument('--profile-directory=WhatsappProfile')
    options.add_argument('--no-first-run')
    options.add_argument('--no-service-autorun')
    options.add_argument('--headless=new')  # Run in headless mode for mobile
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    return webdriver.Chrome(options=options)

def send_whatsapp_message(driver, phone, message):
    try:
        print(f"Preparing to send message to {phone}")
        encoded_message = message.replace(' ', '%20').replace('\n', '%0A')
        url = WHATSAPP_URL.format(phone=phone, text=encoded_message)
        
        driver.get(url)
        
        # Wait for either message input or login requirement
        try:
            WebDriverWait(driver, 30).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]')),
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Use WhatsApp on your computer")]'))
                )
            )
        except TimeoutException:
            raise Exception("WhatsApp Web session timed out - check login status")

        # Check if we need to scan QR code
        if "Use WhatsApp on your computer" in driver.page_source:
            raise Exception("WhatsApp Web not logged in - scan QR code first")
        
        # Wait for message input to be interactable
        input_xpath = '//div[@role="textbox"][@contenteditable="true"]'
        input_box = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, input_xpath))
        )
        
        # Clear existing text and send message with Enter key
        input_box.send_keys(Keys.CONTROL + 'a')
        input_box.send_keys(Keys.BACKSPACE)
        input_box.send_keys(message)
        input_box.send_keys(Keys.ENTER)
        
        print("Message sent successfully")
        return True

    except Exception as e:
        print(f"Error during sending: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        if len(sys.argv) != 3:
            raise Exception("Requires 2 arguments: phone_number message")
            
        _, phone, message = sys.argv
        
        if not phone.startswith("+"):
            raise ValueError("Phone number must include country code (e.g. +1234567890)")
            
        driver = initialize_driver()
        success = send_whatsapp_message(driver, phone, message)
        
        # Cleanup
        time.sleep(2)  # Allow time for message to send
        driver.close()
        driver.quit()
        
        sys.exit(0 if success else 1)

    except Exception as e:
        print(f"Execution failed: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        sys.exit(1)