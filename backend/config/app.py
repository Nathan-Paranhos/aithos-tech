import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Carrega variáveis de ambiente
load_dotenv()

class Settings(BaseSettings):
    # Configurações do aplicativo
    APP_NAME: str = "AgroGuard API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API para o sistema de manutenção preditiva AgroGuard"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # Configurações do servidor
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    API_PREFIX: str = "/api/v1"
    
    # Configurações de segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "sua_chave_secreta_aqui")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias
    
    # Configurações de CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://agroguard.vercel.app",
        "*"
    ]
    
    # Configurações de notificação
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER", "")
    
    # Configurações de email
    EMAIL_USER: str = os.getenv("EMAIL_USER", "")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Cria uma instância das configurações
settings = Settings()