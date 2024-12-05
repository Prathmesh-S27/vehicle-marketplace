from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict

from ..database import get_db
from ..services.auth_service import AuthService
from ..services.otp_service import OTPService
from ..models.user import User
from ..schemas.user_schema import UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/send-otp")
def send_otp(
    mobile_number: str, 
    db: Session = Depends(get_db)
):
    # Check if user exists, if not create
    user = db.query(User).filter(User.mobile_number == mobile_number).first()
    
    if not user:
        user_create = UserCreate(mobile_number=mobile_number)
        user = AuthService.create_user(db, user_create)
    
    # Generate and send OTP
    if OTPService.send_otp(mobile_number):
        return {"message": "OTP sent successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail="Failed to send OTP"
    )

@router.post("/verify-otp")
def verify_otp(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    # Verify OTP
    if not OTPService.verify_otp(
        login_data.mobile_number, 
        login_data.otp
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid or expired OTP"
        )
    
    # Find user
    user = db.query(User).filter(
        User.mobile_number == login_data.mobile_number
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    # Generate JWT token
    token = AuthService.generate_jwt_token(user)
    
    return {
        "token": token,
        "user": {
            "id": user.id,
            "mobile_number": user.mobile_number,
            "role": user.role
        }
    }
