from fastapi import APIRouter, Depends, HTTPException, status, Body, Query, Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from models.maintenance import MaintenanceCreate, MaintenanceUpdate, Maintenance
from services import MaintenanceService
from services.auth_service import get_current_user

router = APIRouter(prefix="/maintenance", tags=["maintenance"])

@router.post("/", response_model=Maintenance)
async def create_maintenance(
    maintenance_data: MaintenanceCreate = Body(...),
    current_user: str = Depends(get_current_user)
):
    """Cria um novo registro de manutenção"""
    return await MaintenanceService.create_maintenance(maintenance_data, current_user)

@router.get("/", response_model=List[Maintenance])
async def get_all_maintenance(
    current_user: str = Depends(get_current_user),
    equipment_id: Optional[str] = Query(None, description="Filtrar por equipamento"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    maintenance_type: Optional[str] = Query(None, description="Filtrar por tipo de manutenção"),
    from_date: Optional[datetime] = Query(None, description="Data inicial para filtro"),
    to_date: Optional[datetime] = Query(None, description="Data final para filtro")
):
    """Retorna todos os registros de manutenção do usuário, com opções de filtro"""
    return await MaintenanceService.get_all_maintenance(
        current_user, 
        equipment_id=equipment_id, 
        status=status, 
        maintenance_type=maintenance_type,
        from_date=from_date,
        to_date=to_date
    )

@router.get("/stats", response_model=Dict[str, Any])
async def get_maintenance_stats(current_user: str = Depends(get_current_user)):
    """Retorna estatísticas de manutenção do usuário"""
    return await MaintenanceService.get_maintenance_statistics(current_user)

@router.get("/upcoming", response_model=List[Maintenance])
async def get_upcoming_maintenance(
    current_user: str = Depends(get_current_user),
    days: int = Query(30, description="Número de dias para considerar como próximos")
):
    """Retorna as manutenções programadas para os próximos dias"""
    return await MaintenanceService.get_upcoming_maintenance(current_user, days)

@router.get("/{maintenance_id}", response_model=Maintenance)
async def get_maintenance(
    maintenance_id: str = Path(..., description="ID da manutenção"),
    current_user: str = Depends(get_current_user)
):
    """Retorna um registro de manutenção específico"""
    return await MaintenanceService.get_maintenance_by_id(maintenance_id, current_user)

@router.put("/{maintenance_id}", response_model=Maintenance)
async def update_maintenance(
    maintenance_data: MaintenanceUpdate = Body(...),
    maintenance_id: str = Path(..., description="ID da manutenção"),
    current_user: str = Depends(get_current_user)
):
    """Atualiza um registro de manutenção específico"""
    return await MaintenanceService.update_maintenance(maintenance_id, maintenance_data, current_user)

@router.delete("/{maintenance_id}", response_model=Dict[str, Any])
async def delete_maintenance(
    maintenance_id: str = Path(..., description="ID da manutenção"),
    current_user: str = Depends(get_current_user)
):
    """Remove um registro de manutenção específico"""
    return await MaintenanceService.delete_maintenance(maintenance_id, current_user)

@router.post("/{maintenance_id}/complete", response_model=Maintenance)
async def complete_maintenance(
    completion_data: Dict[str, Any] = Body(...),
    maintenance_id: str = Path(..., description="ID da manutenção"),
    current_user: str = Depends(get_current_user)
):
    """Marca uma manutenção como concluída"""
    return await MaintenanceService.complete_maintenance(
        maintenance_id, 
        completion_data.get("technician_notes", ""), 
        completion_data.get("downtime_hours", 0),
        completion_data.get("cost", 0),
        completion_data.get("components_replaced", []),
        current_user
    )

@router.post("/schedule", response_model=List[Maintenance])
async def schedule_maintenance(
    current_user: str = Depends(get_current_user),
    equipment_id: Optional[str] = Query(None, description="ID do equipamento para agendar manutenção específica")
):
    """Agenda manutenções automaticamente com base na análise de risco"""
    return await MaintenanceService.schedule_automatic_maintenance(current_user, equipment_id)

@router.get("/equipment/{equipment_id}", response_model=List[Maintenance])
async def get_equipment_maintenance_history(
    equipment_id: str = Path(..., description="ID do equipamento"),
    current_user: str = Depends(get_current_user),
    limit: int = Query(10, description="Número de registros a retornar")
):
    """Retorna o histórico de manutenção de um equipamento específico"""
    return await MaintenanceService.get_equipment_maintenance_history(equipment_id, current_user, limit)