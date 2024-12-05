from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict

from ...database import get_db
from ...services.auth_service import AuthService
from ...models.user import User
from ...schemas.user_schema import UserCreate, UserLogin

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
    
    # Generate OTP
    otp = AuthService.generate_otp()
    
    # TODO: Implement actual OTP sending via SMS service
    print(f"OTP for {mobile_number}: {otp}")
    
    return {"message": "OTP sent successfully"}

@router.post("/verify-otp")
def verify_otp(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    # In a real-world scenario, you'd validate the OTP
    # Here we're simulating OTP verification
    user = db.query(User).filter(User.mobile_number == login_data.mobile_number).first()
    
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

@router.post("/validate-token")
def validate_token(
    token: Dict[str, str],
    db: Session = Depends(get_db)
):
    payload = AuthService.verify_jwt_token(token['token'])
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or expired token"
        )
    
    user = db.query(User).filter(User.id == payload['user_id']).first()
    
    return {
        "valid": True,
        "role": user.role
    }
