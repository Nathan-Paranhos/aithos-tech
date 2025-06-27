from fastapi import APIRouter, Depends, HTTPException, status, Body, Query, Path
from typing import List, Dict, Any, Optional

from models.equipment import EquipmentCreate, EquipmentUpdate, Equipment, OperationalData
from services.equipment_service import EquipmentService
from services.auth_service import get_current_user  # Correção aqui
from models.user import User

router = APIRouter(prefix="/equipment", tags=["equipment"])

@router.post("/", response_model=Equipment)
async def create_equipment(
    equipment_data: EquipmentCreate = Body(...),
    current_user: User = Depends(get_current_user)
):
    return await EquipmentService.create_equipment(equipment_data, current_user.id)

@router.get("/", response_model=List[Equipment])
async def get_all_equipment(
    current_user: User = Depends(get_current_user),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    risk_level: Optional[str] = Query(None, description="Filtrar por nível de risco")
):
    return await EquipmentService.get_all_equipment(
        current_user.id, category=category, status=status, risk_level=risk_level
    )

@router.get("/stats", response_model=Dict[str, Any])
async def get_equipment_stats(current_user: User = Depends(get_current_user)):
    return await EquipmentService.get_equipment_statistics(current_user.id)

@router.get("/{equipment_id}", response_model=Equipment)
async def get_equipment(
    equipment_id: str = Path(..., description="ID do equipamento"),
    current_user: User = Depends(get_current_user)
):
    return await EquipmentService.get_equipment_by_id(equipment_id, current_user.id)

@router.put("/{equipment_id}", response_model=Equipment)
async def update_equipment(
    equipment_data: EquipmentUpdate = Body(...),
    equipment_id: str = Path(..., description="ID do equipamento"),
    current_user: User = Depends(get_current_user)
):
    return await EquipmentService.update_equipment(equipment_id, equipment_data, current_user.id)

@router.delete("/{equipment_id}", response_model=Dict[str, Any])
async def delete_equipment(
    equipment_id: str = Path(..., description="ID do equipamento"),
    current_user: User = Depends(get_current_user)
):
    return await EquipmentService.delete_equipment(equipment_id, current_user.id)

@router.post("/{equipment_id}/operational-data", response_model=Equipment)
async def add_operational_data(
    operational_data: OperationalData = Body(...),
    equipment_id: str = Path(..., description="ID do equipamento"),
    current_user: User = Depends(get_current_user)
):
    return await EquipmentService.add_operational_data(equipment_id, operational_data, current_user.id)

@router.get("/{equipment_id}/health-analysis", response_model=Dict[str, Any])
async def analyze_equipment_health(
    equipment_id: str = Path(..., description="ID do equipamento"),
    current_user: User = Depends(get_current_user)
):
    return await EquipmentService.analyze_equipment_health(equipment_id, current_user.id)

@router.post("/{equipment_id}/components", response_model=Equipment)
async def add_component(
    component_data: Dict[str, Any] = Body(...),
    equipment_id: str = Path(..., description="ID do equipamento"),
    current_user: User = Depends(get_current_user)
):
    return await EquipmentService.add_component(equipment_id, component_data, current_user.id)

@router.put("/{equipment_id}/components/{component_id}", response_model=Equipment)
async def update_component(
    component_data: Dict[str, Any] = Body(...),
    equipment_id: str = Path(..., description="ID do equipamento"),
    component_id: str = Path(..., description="ID do componente"),
    current_user: User = Depends(get_current_user)
):
    return await EquipmentService.update_component(equipment_id, component_id, component_data, current_user.id)

@router.delete("/{equipment_id}/components/{component_id}", response_model=Equipment)
async def remove_component(
    equipment_id: str = Path(..., description="ID do equipamento"),
    component_id: str = Path(..., description="ID do componente"),
    current_user: User = Depends(get_current_user)
):
    return await EquipmentService.remove_component(equipment_id, component_id, current_user.id)
