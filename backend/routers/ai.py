from fastapi import APIRouter, Depends, HTTPException, status, Body, Query, Path
from typing import List, Dict, Any, Optional

from services import AIService
from services.auth_service import get_current_user_id  # ✅ ajuste aqui

router = APIRouter(prefix="/ai", tags=["ai"])

@router.get("/predict/{equipment_id}", response_model=Dict[str, Any])
async def predict_equipment_failure(
    equipment_id: str = Path(..., description="ID do equipamento"),
    user_id: str = Depends(get_current_user_id),  # ✅ ajuste aqui
    days_ahead: int = Query(30, description="Número de dias para previsão")
):
    """Prevê a probabilidade de falha de um equipamento nos próximos X dias"""
    return await AIService.predict_equipment_failure(equipment_id, days_ahead)

@router.get("/maintenance-schedule/{equipment_id}", response_model=Dict[str, Any])
async def recommend_maintenance_schedule(
    equipment_id: str = Path(..., description="ID do equipamento"),
    user_id: str = Depends(get_current_user_id)
):
    """Recomenda um cronograma de manutenção para o equipamento"""
    return await AIService.recommend_maintenance_schedule(equipment_id)

@router.get("/analyze/{equipment_id}", response_model=Dict[str, Any])
async def analyze_operational_data(
    equipment_id: str = Path(..., description="ID do equipamento"),
    user_id: str = Depends(get_current_user_id)
):
    """Analisa dados operacionais para identificar padrões e anomalias"""
    return await AIService.analyze_operational_data(equipment_id)

@router.post("/train/{equipment_id}", response_model=Dict[str, Any])
async def train_custom_model(
    equipment_id: str = Path(..., description="ID do equipamento"),
    user_id: str = Depends(get_current_user_id)
):
    """Treina um modelo personalizado para um equipamento específico"""
    return await AIService.train_custom_model(equipment_id, user_id)
