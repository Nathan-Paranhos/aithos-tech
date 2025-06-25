from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class EquipmentBase(BaseModel):
    name: str
    model: str
    manufacturer: str
    description: Optional[str] = None
    category: Optional[str] = None
    year: Optional[int] = None
    serial_number: Optional[str] = None

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    year: Optional[int] = None
    serial_number: Optional[str] = None
    status: Optional[str] = None
    risk_level: Optional[str] = None
    needs_maintenance: Optional[bool] = None
    last_maintenance_date: Optional[datetime] = None
    next_maintenance_date: Optional[datetime] = None

class EquipmentComponent(BaseModel):
    name: str
    estimated_lifetime_hours: float
    current_usage_hours: float
    health_percentage: float
    risk_level: str
    estimated_replacement_date: Optional[datetime] = None
    last_replacement_date: Optional[datetime] = None

class OperationalData(BaseModel):
    date: datetime
    hours_used: float
    temperature: Optional[float] = None
    consumption: Optional[float] = None
    noise_level: Optional[float] = None
    vibration: Optional[float] = None
    cycles: Optional[int] = None
    additional_data: Optional[Dict[str, Any]] = None

class Equipment(EquipmentBase):
    id: str
    user_id: str
    status: str = "active"  # active, inactive, maintenance, retired
    risk_level: str = "low"  # low, medium, high
    needs_maintenance: bool = False
    components: List[EquipmentComponent] = []
    operational_data: List[OperationalData] = []
    mttf: Optional[float] = None  # Mean Time To Failure in hours
    maintenance_cycle: Optional[int] = None  # Recommended days between maintenance
    total_usage_hours: float = 0
    last_maintenance_date: Optional[datetime] = None
    next_maintenance_date: Optional[datetime] = None
    failure_history: List[Dict[str, Any]] = [] # Adicionar histórico de falhas
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True