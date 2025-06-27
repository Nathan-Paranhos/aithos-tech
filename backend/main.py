from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import os
import firebase_admin
from firebase_admin import credentials, firestore

# Serviços e modelos
from services.auth_service import get_current_user, create_access_token
from services.equipment_service import EquipmentService
from services.alert_service import AlertService
from services.maintenance_service import MaintenanceService
from services.ai_service import AIService
from services.notification_service import NotificationService
from services.report_service import ReportService

# Rotas
from routers import auth, equipment, alert, maintenance, report

# Inicialização do Firebase Admin SDK
cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase-credentials.json")

if os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
else:
    cred = credentials.Certificate({
        "type": os.getenv("FIREBASE_TYPE"),
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
        "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
        "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL"),
        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL")
    })

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Inicializa Firestore
db = firestore.client()

# Criação do app FastAPI
app = FastAPI(
    title="AgroGuard API",
    description="API para manutenção preditiva de equipamentos industriais, agrícolas e automotivos",
    version="1.0.0"
)

# Middleware de CORS
import json

# Obter origens permitidas do arquivo .env
try:
    cors_origins_str = os.getenv("CORS_ORIGINS", '["http://localhost:3000", "https://agroguard.com", "https://www.agroguard.com"]')
    cors_origins = json.loads(cors_origins_str)
    print(f"CORS origins configuradas: {cors_origins}")
except json.JSONDecodeError as e:
    print(f"Erro ao decodificar CORS_ORIGINS: {e}. Usando valores padrão.")
    cors_origins = ["http://localhost:3000", "https://agroguard.com", "https://www.agroguard.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
    expose_headers=["Content-Disposition"],
    max_age=600,  # Cache preflight por 10 minutos
)

# Registro de rotas
app.include_router(auth.router)
app.include_router(equipment.router)
app.include_router(alert.router)
app.include_router(maintenance.router)
app.include_router(report.router)

# Endpoint raiz
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do AgroGuard - Manutenção Preditiva Inteligente"}

# Endpoint de saúde
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Manipulador global de exceções
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Ocorreu um erro interno: {str(exc)}"},
    )

# Execução direta
if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    import os
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Obter configurações do servidor
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8010"))
    debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # Iniciar o servidor
    uvicorn.run("main:app", host=host, port=port, reload=debug)
