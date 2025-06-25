from fastapi import APIRouter, Depends, HTTPException, status, Body, Query, Path
from typing import List, Dict, Any, Optional

from models.equipment import EquipmentCreate, EquipmentUpdate, Equipment, OperationalData
from services import EquipmentService, AuthService

router = APIRouter(prefix="/equipment", tags=["equipment"])

@router.post("/", response_model=Equipment)
async def create_equipment(
    equipment_data: EquipmentCreate = Body(...),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Cria um novo equipamento"""
    return await EquipmentService.create_equipment(equipment_data, user_id)

@router.get("/", response_model=List[Equipment])
async def get_all_equipment(
    user_id: str = Depends(AuthService.get_current_user_id),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    risk_level: Optional[str] = Query(None, description="Filtrar por nível de risco")
):
    """Retorna todos os equipamentos do usuário, com opções de filtro"""
    return await EquipmentService.get_all_equipment(
        user_id, category=category, status=status, risk_level=risk_level
    )

@router.get("/stats", response_model=Dict[str, Any])
async def get_equipment_stats(user_id: str = Depends(AuthService.get_current_user_id)):
    """Retorna estatísticas dos equipamentos do usuário"""
    return await EquipmentService.get_equipment_statistics(user_id)

@router.get("/{equipment_id}", response_model=Equipment)
async def get_equipment(
    equipment_id: str = Path(..., description="ID do equipamento"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Retorna um equipamento específico"""
    return await EquipmentService.get_equipment_by_id(equipment_id, user_id)

@router.put("/{equipment_id}", response_model=Equipment)
async def update_equipment(
    equipment_data: EquipmentUpdate = Body(...),
    equipment_id: str = Path(..., description="ID do equipamento"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Atualiza um equipamento específico"""
    return await EquipmentService.update_equipment(equipment_id, equipment_data, user_id)

@router.delete("/{equipment_id}", response_model=Dict[str, Any])
async def delete_equipment(
    equipment_id: str = Path(..., description="ID do equipamento"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Remove um equipamento específico"""
    return await EquipmentService.delete_equipment(equipment_id, user_id)

@router.post("/{equipment_id}/operational-data", response_model=Equipment)
async def add_operational_data(
    operational_data: OperationalData = Body(...),
    equipment_id: str = Path(..., description="ID do equipamento"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Adiciona dados operacionais a um equipamento"""
    return await EquipmentService.add_operational_data(equipment_id, operational_data, user_id)

@router.get("/{equipment_id}/health-analysis", response_model=Dict[str, Any])
async def analyze_equipment_health(
    equipment_id: str = Path(..., description="ID do equipamento"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Analisa a saúde de um equipamento específico"""
    return await EquipmentService.analyze_equipment_health(equipment_id, user_id)

@router.post("/{equipment_id}/components", response_model=Equipment)
async def add_component(
    component_data: Dict[str, Any] = Body(...),
    equipment_id: str = Path(..., description="ID do equipamento"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Adiciona um componente a um equipamento"""
    return await EquipmentService.add_component(equipment_id, component_data, user_id)

@router.put("/{equipment_id}/components/{component_id}", response_model=Equipment)
async def update_component(
    component_data: Dict[str, Any] = Body(...),
    equipment_id: str = Path(..., description="ID do equipamento"),
    component_id: str = Path(..., description="ID do componente"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Atualiza um componente específico de um equipamento"""
    return await EquipmentService.update_component(equipment_id, component_id, component_data, user_id)

@router.delete("/{equipment_id}/components/{component_id}", response_model=Equipment)
async def remove_component(
    equipment_id: str = Path(..., description="ID do equipamento"),
    component_id: str = Path(..., description="ID do componente"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Remove um componente específico de um equipamento"""
    return await EquipmentService.remove_component(equipment_id, component_id, user_id)