from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ReportBase(BaseModel):
    equipment_id: str
    report_type: str  # health, maintenance, prediction, summary
    title: str

class ReportCreate(ReportBase):
    pass

class ReportUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    content: Optional[Dict[str, Any]] = None

class Report(ReportBase):
    id: str
    user_id: str
    equipment_name: str
    status: str = "generated"  # generated, viewed, archived
    content: Dict[str, Any] = {}
    file_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    viewed_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class HealthReportContent(BaseModel):
    overall_health: float  # 0-100%
    risk_level: str  # low, medium, high
    components_health: Dict[str, float]
    critical_components: List[str]
    operational_metrics: Dict[str, Any]
    recommendations: List[str]
    historical_trend: List[Dict[str, Any]]

class MaintenanceReportContent(BaseModel):
    last_maintenance_date: Optional[datetime] = None
    next_maintenance_date: Optional[datetime] = None
    maintenance_history: List[Dict[str, Any]]
    components_replaced: List[Dict[str, Any]]
    total_maintenance_cost: float
    downtime_hours: float
    maintenance_efficiency: Optional[float] = None  # 0-100%

class PredictionReportContent(BaseModel):
    predicted_failures: List[Dict[str, Any]]
    reliability_score: float  # 0-100%
    estimated_lifetime_remaining: Dict[str, Any]
    risk_factors: List[Dict[str, Any]]
    confidence_level: float  # 0-100%
    data_points_analyzed: int