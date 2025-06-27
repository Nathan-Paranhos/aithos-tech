import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Carrega variáveis do arquivo .env
load_dotenv()

class Settings(BaseSettings):
    # App
    APP_NAME: str = os.getenv("APP_NAME", "AgroGuard")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION", "Sistema de monitoramento preditivo para equipamentos agrícolas")

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")

    # Segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    # Firebase
    FIREBASE_TYPE: str = os.getenv("FIREBASE_TYPE")
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_PRIVATE_KEY_ID: str = os.getenv("FIREBASE_PRIVATE_KEY_ID")
    FIREBASE_PRIVATE_KEY: str = os.getenv("FIREBASE_PRIVATE_KEY", "").replace('\\n', '\n')
    FIREBASE_CLIENT_EMAIL: str = os.getenv("FIREBASE_CLIENT_EMAIL")
    FIREBASE_CLIENT_ID: str = os.getenv("FIREBASE_CLIENT_ID")
    FIREBASE_AUTH_URI: str = os.getenv("FIREBASE_AUTH_URI")
    FIREBASE_TOKEN_URI: str = os.getenv("FIREBASE_TOKEN_URI")
    FIREBASE_AUTH_PROVIDER_CERT_URL: str = os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL")
    FIREBASE_CLIENT_CERT_URL: str = os.getenv("FIREBASE_CLIENT_CERT_URL")

    # Email
    EMAIL_HOST: str = os.getenv("EMAIL_HOST")
    EMAIL_PORT: int = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_USERNAME: str = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM")

    # Twilio
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER")

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "allow"  # Permite campos extras
    }

settings = Settings()
