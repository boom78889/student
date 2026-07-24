import os
from twilio.rest import Client

def send_otp_sms(phone_number, otp_code):
    """
    Send OTP via SMS using Twilio
    
    Args:
        phone_number: Recipient's phone number
        otp_code: 6-digit OTP code
    """
    try:
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, twilio_number]):
            print("Warning: Twilio credentials not configured")
            return False
        
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=f"Your Hotel Management App OTP is: {otp_code}. Valid for 10 minutes.",
            from_=twilio_number,
            to=phone_number
        )
        
        print(f"SMS sent successfully. Message ID: {message.sid}")
        return True
    
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return False
