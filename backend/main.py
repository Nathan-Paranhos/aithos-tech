from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth
import os
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb
from models.equipment import Equipment, EquipmentCreate, EquipmentUpdate
from models.user import User, UserCreate
from models.alert import Alert, AlertCreate
from models.maintenance import Maintenance, MaintenanceCreate
from services.auth_service import get_current_user, create_access_token
from services.equipment_service import EquipmentService
from services.alert_service import AlertService
from services.maintenance_service import MaintenanceService
from services.ai_service import AIService
from services.notification_service import NotificationService
from services.report_service import ReportService
from services.data_collection_service import DataCollectionService
from routers import auth, equipment, alerts, maintenance, reports

# Initialize Firebase Admin SDK
cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase-credentials.json")

# Check if running in production or development
if os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
else:
    # Use environment variables for production
    cred_dict = {
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
    }
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

# Create FastAPI app
app = FastAPI(
    title="AgroGuard API",
    description="API para manutenção preditiva de equipamentos industriais, agrícolas e automotivos",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(equipment.router)
app.include_router(alerts.router)
app.include_router(maintenance.router)
app.include_router(reports.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do AgroGuard - Manutenção Preditiva Inteligente"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Ocorreu um erro interno: {str(exc)}"},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)