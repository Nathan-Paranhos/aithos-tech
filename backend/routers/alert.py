from fastapi import APIRouter, Depends, HTTPException, status, Body, Query, Path
from typing import List, Dict, Any, Optional

from models.alert import AlertCreate, AlertUpdate, Alert
from services import AlertService, AuthService

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.post("/", response_model=Alert)
async def create_alert(
    alert_data: AlertCreate = Body(...),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Cria um novo alerta"""
    return await AlertService.create_alert(alert_data, user_id)

@router.get("/", response_model=List[Alert])
async def get_all_alerts(
    user_id: str = Depends(AuthService.get_current_user_id),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    severity: Optional[str] = Query(None, description="Filtrar por severidade"),
    equipment_id: Optional[str] = Query(None, description="Filtrar por equipamento")
):
    """Retorna todos os alertas do usuário, com opções de filtro"""
    return await AlertService.get_all_alerts(
        user_id, status=status, severity=severity, equipment_id=equipment_id
    )

@router.get("/stats", response_model=Dict[str, Any])
async def get_alert_stats(user_id: str = Depends(AuthService.get_current_user_id)):
    """Retorna estatísticas dos alertas do usuário"""
    return await AlertService.get_alert_statistics(user_id)

@router.get("/recent", response_model=List[Alert])
async def get_recent_alerts(
    user_id: str = Depends(AuthService.get_current_user_id),
    limit: int = Query(5, description="Número de alertas recentes a retornar")
):
    """Retorna os alertas mais recentes do usuário"""
    return await AlertService.get_recent_alerts(user_id, limit)

@router.get("/{alert_id}", response_model=Alert)
async def get_alert(
    alert_id: str = Path(..., description="ID do alerta"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Retorna um alerta específico"""
    return await AlertService.get_alert_by_id(alert_id, user_id)

@router.put("/{alert_id}", response_model=Alert)
async def update_alert(
    alert_data: AlertUpdate = Body(...),
    alert_id: str = Path(..., description="ID do alerta"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Atualiza um alerta específico"""
    return await AlertService.update_alert(alert_id, alert_data, user_id)

@router.delete("/{alert_id}", response_model=Dict[str, Any])
async def delete_alert(
    alert_id: str = Path(..., description="ID do alerta"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Remove um alerta específico"""
    return await AlertService.delete_alert(alert_id, user_id)

@router.post("/{alert_id}/resolve", response_model=Alert)
async def resolve_alert(
    resolution_notes: Dict[str, str] = Body(...),
    alert_id: str = Path(..., description="ID do alerta"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Marca um alerta como resolvido"""
    if "notes" not in resolution_notes:
        resolution_notes["notes"] = ""
    
    return await AlertService.resolve_alert(alert_id, resolution_notes["notes"], user_id)

@router.post("/generate", response_model=List[Alert])
async def generate_alerts(
    user_id: str = Depends(AuthService.get_current_user_id),
    equipment_id: Optional[str] = Query(None, description="ID do equipamento para gerar alertas específicos")
):
    """Gera alertas automaticamente com base na análise de equipamentos"""
    return await AlertService.generate_automatic_alerts(user_id, equipment_id)

@router.post("/{alert_id}/notify", response_model=Dict[str, Any])
async def send_notification(
    alert_id: str = Path(..., description="ID do alerta"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Envia uma notificação para o alerta especificado"""
    return await AlertService.send_alert_notification(alert_id, user_id)