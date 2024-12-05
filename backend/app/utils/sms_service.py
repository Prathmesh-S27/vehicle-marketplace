import requests
from ..core.config import settings
from ..utils.logger import logger

class SMSService:
    @staticmethod
    def send_otp(mobile_number: str, otp: str):
        """
        Send OTP via SMS provider
        """
        try:
            response = requests.post(
                settings.SMS_PROVIDER_URL,
                json={
                    "apiKey": settings.SMS_PROVIDER_API_KEY,
                    "mobile": mobile_number,
                    "message": f"Your OTP is {otp}"
                }
            )
            
            if response.status_code == 200:
                logger.info(f"OTP sent successfully to {mobile_number}")
                return True
            else:
                logger.error(f"Failed to send OTP: {response.text}")
                return False
        except Exception as e:
            logger.error(f"SMS sending error: {str(e)}")
            return False
