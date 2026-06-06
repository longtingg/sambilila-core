import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def send_parent_sms(phone_number, message):
    """
    Service to push SMS to Zambian mobile networks.
    Expects phone_number in international format (e.g., +26097...)
    """
    if not phone_number:
        logger.warning("Attempted to send SMS, but no phone number was provided.")
        return False

    # Example integration using a standard HTTP API (like Africa's Talking)
    api_url = "https://api.africastalking.com/version1/messaging"
    
    headers = {
        "ApiKey": settings.SMS_API_KEY, 
        "Accept": "application/json"
    }
    
    payload = {
        "username": settings.SMS_API_USERNAME,
        "to": phone_number,
        "message": message,
        "from": "SAMBILILA" # Your registered alphanumeric sender ID
    }

    try:
        response = requests.post(api_url, headers=headers, data=payload, timeout=5)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"SMS Gateway Failed: {e}")
        return False
