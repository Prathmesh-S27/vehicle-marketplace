from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    # Database Settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://user:password@localhost/vehicle_marketplace"
    )
    
    # Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # SMS Provider Settings
    SMS_PROVIDER_API_KEY: str = os.getenv("SMS_PROVIDER_API_KEY", "")
    SMS_PROVIDER_URL: str = os.getenv("SMS_PROVIDER_URL", "")

    # Image Upload Settings
    UPLOAD_DIRECTORY: str = os.getenv("UPLOAD_DIRECTORY", "/tmp/uploads")
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", 10))

    # Logging Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "/tmp/app.log")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
