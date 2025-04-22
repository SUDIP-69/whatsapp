import pywhatkit
import time
from datetime import datetime

def send_whatsapp_message(phone_number, message):
    try:
        # Ensure the phone number is in the correct format (with country code)
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
            
        # Get current time
        now = datetime.now()
        
        # Send message (will open in new browser instance)
        pywhatkit.sendwhatmsg(
            phone_number,
            message,
            now.hour,
            now.minute + 1,  # Send message 1 minute from now
            15,  # Wait 15 seconds for WhatsApp Web to load
            True,  # Close tab after sending
            True   # Close entire browser after sending
        )
        
        print(f"Message sent successfully to {phone_number}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Get phone number and message from user
    phone = input("Enter phone number (with country code, e.g., +1234567890): ")
    message = input("Enter your message: ")
    
    # Send the message
    send_whatsapp_message(phone, message)