import random
import time
from typing import Dict
from ..core.config import settings
from ..utils.logger import logger
from ..utils.sms_service import SMSService

class OTPService:
    # In-memory OTP storage (in production, use Redis or a distributed cache)
    _otp_storage: Dict[str, Dict[str, str]] = {}

    @classmethod
    def generate_otp(cls, mobile_number: str, length: int = 6) -> str:
        """
        Generate a random OTP for the given mobile number
        """
        # Generate OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
        
        # Store OTP with timestamp
        cls._otp_storage[mobile_number] = {
            'otp': otp,
            'created_at': time.time()
        }
        
        logger.info(f"OTP generated for {mobile_number}")
        return otp

    @classmethod
    def verify_otp(cls, mobile_number: str, user_otp: str) -> bool:
        """
        Verify OTP for a given mobile number
        """
        # Check if OTP exists for mobile number
        stored_otp_data = cls._otp_storage.get(mobile_number)
        
        if not stored_otp_data:
            logger.warning(f"No OTP found for {mobile_number}")
            return False
        
        # Check OTP expiration (5 minutes)
        current_time = time.time()
        if current_time - stored_otp_data['created_at'] > 300:
            logger.warning(f"OTP expired for {mobile_number}")
            del cls._otp_storage[mobile_number]
            return False
        
        # Compare OTPs
        is_valid = stored_otp_data['otp'] == user_otp
        
        # Clear OTP after verification
        if is_valid:
            del cls._otp_storage[mobile_number]
            logger.info(f"OTP verified for {mobile_number}")
        
        return is_valid

    @classmethod
    def send_otp(cls, mobile_number: str) -> bool:
        """
        Generate and send OTP via SMS
        """
        # Generate OTP
        otp = cls.generate_otp(mobile_number)
        
        # Send OTP via SMS
        try:
            return SMSService.send_otp(mobile_number, otp)
        except Exception as e:
            logger.error(f"Failed to send OTP: {str(e)}")
            return False
