import sys
import time
import pywhatkit as pwk
from selenium.common.exceptions import WebDriverException

try:
    phone = sys.argv[1]
    message = sys.argv[2]
    
    print(f"Attempting to send to {phone}...")
    
    pwk.sendwhatmsg_instantly(
        phone_no=phone,
        message=message,
        wait_time=20,
        tab_close=True,
        close_time=3
    )
    
    print("Success: Message queued for sending")
    time.sleep(5)  # Allow time for sending
    sys.exit(0)
    
except WebDriverException as e:
    print(f"Browser Error: {str(e)}")
    print("Ensure: 1) Chrome is installed 2) WhatsApp Web is logged in")
    sys.exit(1)
    
except Exception as e:
    print(f"General Error: {str(e)}")
    sys.exit(1)