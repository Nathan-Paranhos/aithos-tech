from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AlertBase(BaseModel):
    equipment_id: str
    message: str
    severity: str  # high, medium, low
    component: Optional[str] = None
    predicted_failure_days: Optional[int] = None
    recommended_action: Optional[str] = None

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    message: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    component: Optional[str] = None
    predicted_failure_days: Optional[int] = None
    recommended_action: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None

class Alert(AlertBase):
    id: str
    user_id: str
    equipment_name: str
    status: str = "active"  # active, acknowledged, resolved
    created_at: datetime
    updated_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    notification_sent: bool = False
    notification_sent_at: Optional[datetime] = None

    class Config:
        orm_mode = True