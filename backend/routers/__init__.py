from .auth import router as auth_router
from .equipment import router as equipment_router
from .alert import router as alert_router
from .maintenance import router as maintenance_router
from .report import router as report_router
from .ai import router as ai_router

__all__ = [
    'auth_router',
    'equipment_router',
    'alert_router',
    'maintenance_router',
    'report_router',
    'ai_router'
]