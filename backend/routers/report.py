from fastapi import APIRouter, Depends, HTTPException, status, Body, Query, Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from models.report import ReportCreate, ReportUpdate, Report
from services import ReportService, AuthService

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/", response_model=Report)
async def create_report(
    report_data: ReportCreate = Body(...),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Cria um novo relatório"""
    return await ReportService.create_report(report_data, user_id)

@router.get("/", response_model=List[Report])
async def get_all_reports(
    user_id: str = Depends(AuthService.get_current_user_id),
    equipment_id: Optional[str] = Query(None, description="Filtrar por equipamento"),
    report_type: Optional[str] = Query(None, description="Filtrar por tipo de relatório"),
    from_date: Optional[datetime] = Query(None, description="Data inicial para filtro"),
    to_date: Optional[datetime] = Query(None, description="Data final para filtro")
):
    """Retorna todos os relatórios do usuário, com opções de filtro"""
    return await ReportService.get_all_reports(
        user_id, 
        equipment_id=equipment_id, 
        report_type=report_type,
        from_date=from_date,
        to_date=to_date
    )

@router.get("/{report_id}", response_model=Report)
async def get_report(
    report_id: str = Path(..., description="ID do relatório"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Retorna um relatório específico"""
    return await ReportService.get_report_by_id(report_id, user_id)

@router.put("/{report_id}", response_model=Report)
async def update_report(
    report_data: ReportUpdate = Body(...),
    report_id: str = Path(..., description="ID do relatório"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Atualiza um relatório específico"""
    return await ReportService.update_report(report_id, report_data, user_id)

@router.delete("/{report_id}", response_model=Dict[str, Any])
async def delete_report(
    report_id: str = Path(..., description="ID do relatório"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Remove um relatório específico"""
    return await ReportService.delete_report(report_id, user_id)

@router.post("/generate/health", response_model=Report)
async def generate_health_report(
    equipment_id: str = Query(..., description="ID do equipamento"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Gera um relatório de saúde para um equipamento específico"""
    return await ReportService.generate_health_report(equipment_id, user_id)

@router.post("/generate/maintenance", response_model=Report)
async def generate_maintenance_report(
    equipment_id: str = Query(..., description="ID do equipamento"),
    user_id: str = Depends(AuthService.get_current_user_id),
    from_date: Optional[datetime] = Query(None, description="Data inicial para o relatório"),
    to_date: Optional[datetime] = Query(None, description="Data final para o relatório")
):
    """Gera um relatório de manutenção para um equipamento específico"""
    return await ReportService.generate_maintenance_report(equipment_id, user_id, from_date, to_date)

@router.post("/generate/prediction", response_model=Report)
async def generate_prediction_report(
    equipment_id: str = Query(..., description="ID do equipamento"),
    user_id: str = Depends(AuthService.get_current_user_id),
    days_ahead: int = Query(90, description="Número de dias para previsão")
):
    """Gera um relatório de previsão para um equipamento específico"""
    return await ReportService.generate_prediction_report(equipment_id, user_id, days_ahead)

@router.post("/generate/summary", response_model=Report)
async def generate_summary_report(
    user_id: str = Depends(AuthService.get_current_user_id),
    from_date: Optional[datetime] = Query(None, description="Data inicial para o relatório"),
    to_date: Optional[datetime] = Query(None, description="Data final para o relatório")
):
    """Gera um relatório resumido de todos os equipamentos"""
    return await ReportService.generate_summary_report(user_id, from_date, to_date)

@router.get("/{report_id}/pdf", response_model=Dict[str, Any])
async def generate_pdf(
    report_id: str = Path(..., description="ID do relatório"),
    user_id: str = Depends(AuthService.get_current_user_id)
):
    """Gera uma versão PDF de um relatório específico"""
    return await ReportService.generate_pdf_report(report_id, user_id)

@router.get("/equipment/{equipment_id}", response_model=List[Report])
async def get_equipment_reports(
    equipment_id: str = Path(..., description="ID do equipamento"),
    user_id: str = Depends(AuthService.get_current_user_id),
    limit: int = Query(10, description="Número de relatórios a retornar")
):
    """Retorna os relatórios de um equipamento específico"""
    return await ReportService.get_equipment_reports(equipment_id, user_id, limit)