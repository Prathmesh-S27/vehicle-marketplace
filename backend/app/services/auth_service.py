import random
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user_schema import UserCreate
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
OTP_EXPIRATION = 10  # minutes

class AuthService:
    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        db_user = User(
            mobile_number=user.mobile_number,
            role=user.role or "user"
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def generate_jwt_token(user: User):
        payload = {
            "user_id": user.id,
            "mobile_number": user.mobile_number,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def verify_jwt_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
