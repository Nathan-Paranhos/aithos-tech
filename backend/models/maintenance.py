from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class MaintenanceBase(BaseModel):
    equipment_id: str
    maintenance_type: str  # preventive, corrective, predictive
    description: str
    components_replaced: Optional[List[str]] = None
    cost: Optional[float] = None

class MaintenanceCreate(MaintenanceBase):
    scheduled_date: Optional[datetime] = None

class MaintenanceUpdate(BaseModel):
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    components_replaced: Optional[List[str]] = None
    cost: Optional[float] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    technician_notes: Optional[str] = None
    downtime_hours: Optional[float] = None

class Maintenance(MaintenanceBase):
    id: str
    user_id: str
    equipment_name: str
    status: str = "scheduled"  # scheduled, in_progress, completed, cancelled
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    technician_notes: Optional[str] = None
    downtime_hours: Optional[float] = None
    related_alert_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    additional_data: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True