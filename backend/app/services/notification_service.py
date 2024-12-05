from typing import List, Optional
from ..models.user import User
from ..models.contact_request import ContactRequest
from ..database import SessionLocal
from ..utils.logger import logger
from ..utils.sms_service import SMSService
from ..core.config import settings

class NotificationService:
    @staticmethod
    def send_sms_notification(
        mobile_number: str, 
        message: str
    ) -> bool:
        """
        Send SMS notification to a specific mobile number
        """
        try:
            return SMSService.send_sms(mobile_number, message)
        except Exception as e:
            logger.error(f"SMS notification error: {str(e)}")
            return False

    @staticmethod
    def notify_vehicle_contact_request(
        contact_request: ContactRequest
    ) -> bool:
        """
        Notify seller about a contact request
        """
        try:
            with SessionLocal() as db:
                # Fetch seller details
                seller = db.query(User).filter(
                    User.id == contact_request.vehicle.seller_id
                ).first()
                
                if not seller:
                    logger.warning("Seller not found for contact request")
                    return False
                
                # Compose notification message
                message = (
                    f"New contact request for your vehicle {contact_request.vehicle.model}. "
                    f"Contact: {contact_request.contact_name}, "
                    f"Phone: {contact_request.contact_mobile}"
                )
                
                # Send SMS to seller
                return SMSService.send_sms(
                    seller.mobile_number, 
                    message
                )
        except Exception as e:
            logger.error(f"Contact request notification error: {str(e)}")
            return False

    @staticmethod
    def bulk_sms_notification(
        mobile_numbers: List[str], 
        message: str
    ) -> List[str]:
        """
        Send bulk SMS notifications
        Returns list of failed mobile numbers
        """
        failed_numbers = []
        
        for mobile_number in mobile_numbers:
            try:
                success = SMSService.send_sms(mobile_number, message)
                if not success:
                    failed_numbers.append(mobile_number)
            except Exception as e:
                logger.error(f"Bulk SMS error for {mobile_number}: {str(e)}")
                failed_numbers.append(mobile_number)
        
        return failed_numbers
