import os
import json
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, ClassVar, Any

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Settings(BaseSettings):
    # Configurações do aplicativo
    APP_NAME: str = "AgroGuard API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API para o sistema de manutenção preditiva AgroGuard"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # Configurações do servidor
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8010"))
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")

    # Configurações de segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "sua_chave_secreta_aqui")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias

    # Configurações de CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8010",
        "https://agroguard.com",
        "https://www.agroguard.com",
        "https://api.agroguard.com"
    ]
    
    # Converter string JSON de CORS_ORIGINS do .env, se existir
    if os.getenv("CORS_ORIGINS"):
        try:
            CORS_ORIGINS = json.loads(os.getenv("CORS_ORIGINS"))
        except Exception as e:
            print(f"Erro ao carregar CORS_ORIGINS do .env: {e}")
            # Manter os valores padrão definidos acima

    # Configurações de notificação (Twilio)
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER", "")

    # Configurações de email
    EMAIL_USER: str = os.getenv("EMAIL_USER", "")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "")

    # Configuração do Pydantic Settings (versão 2+)
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",           # permite variáveis extras no .env
        case_sensitive=True
    )

# Instância global das configurações
settings = Settings()
