from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import uuid
import json
import os

from fastapi import HTTPException, status
from firebase_admin import firestore, storage

from config import db, bucket
from models.report import Report, ReportCreate, ReportUpdate, HealthReportContent, MaintenanceReportContent, PredictionReportContent

class ReportService:
    @staticmethod
    async def create_report(user_id: str, report_data: ReportCreate) -> Report:
        try:
            # Gerar ID único para o relatório
            report_id = str(uuid.uuid4())
            
            # Buscar nome do equipamento
            equipment_doc = db.collection("equipment").document(report_data.equipment_id).get()
            
            if not equipment_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Equipamento não encontrado"
                )
            
            equipment_data = equipment_doc.to_dict()
            equipment_name = equipment_data.get("name", "Equipamento desconhecido")
            
            # Verificar se o equipamento pertence ao usuário
            if equipment_data["user_id"] != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Acesso não autorizado a este equipamento"
                )
            
            # Gerar conteúdo do relatório com base no tipo
            content = await ReportService._generate_report_content(
                report_type=report_data.report_type,
                equipment_id=report_data.equipment_id,
                user_id=user_id
            )
            
            # Preparar dados do relatório
            report_dict = report_data.dict()
            report_dict.update({
                "id": report_id,
                "user_id": user_id,
                "equipment_name": equipment_name,
                "status": "generated",
                "content": content,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            
            # Adicionar ao Firestore
            db.collection("reports").document(report_id).set(report_dict)
            
            # Gerar PDF e salvar no Storage (implementação simplificada)
            file_url = await ReportService._generate_pdf(report_id, report_dict)
            
            if file_url:
                db.collection("reports").document(report_id).update({
                    "file_url": file_url
                })
                report_dict["file_url"] = file_url
            
            return Report(**report_dict)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao criar relatório: {str(e)}"
            )
    
    @staticmethod
    async def get_report_by_id(report_id: str, user_id: str) -> Report:
        try:
            report_doc = db.collection("reports").document(report_id).get()
            
            if not report_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Relatório não encontrado"
                )
            
            report_data = report_doc.to_dict()
            
            # Verificar se o relatório pertence ao usuário
            if report_data["user_id"] != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Acesso não autorizado a este relatório"
                )
            
            # Atualizar status para visualizado se ainda não foi
            if report_data["status"] == "generated":
                db.collection("reports").document(report_id).update({
                    "status": "viewed",
                    "viewed_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                })
                report_data["status"] = "viewed"
                report_data["viewed_at"] = datetime.utcnow()
                report_data["updated_at"] = datetime.utcnow()
            
            return Report(**report_data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao buscar relatório: {str(e)}"
            )
    
    @staticmethod
    async def get_all_reports(user_id: str, equipment_id: Optional[str] = None, report_type: Optional[str] = None) -> List[Report]:
        try:
            # Iniciar consulta base
            query = db.collection("reports").where("user_id", "==", user_id)
            
            # Adicionar filtro de equipamento se fornecido
            if equipment_id:
                query = query.where("equipment_id", "==", equipment_id)
            
            # Adicionar filtro de tipo se fornecido
            if report_type:
                query = query.where("report_type", "==", report_type)
            
            # Ordenar por data de criação (mais recentes primeiro)
            query = query.order_by("created_at", direction=firestore.Query.DESCENDING)
            
            # Executar consulta
            report_docs = query.stream()
            
            report_list = []
            for doc in report_docs:
                report_data = doc.to_dict()
                report_list.append(Report(**report_data))
            
            return report_list
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao listar relatórios: {str(e)}"
            )
    
    @staticmethod
    async def update_report(report_id: str, user_id: str, report_data: ReportUpdate) -> Report:
        try:
            # Verificar se o relatório existe e pertence ao usuário
            report = await ReportService.get_report_by_id(report_id, user_id)
            
            # Preparar dados para atualização
            update_data = report_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            # Atualizar no Firestore
            db.collection("reports").document(report_id).update(update_data)
            
            # Buscar relatório atualizado
            updated_report = await ReportService.get_report_by_id(report_id, user_id)
            return updated_report
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao atualizar relatório: {str(e)}"
            )
    
    @staticmethod
    async def delete_report(report_id: str, user_id: str) -> Dict[str, str]:
        try:
            # Verificar se o relatório existe e pertence ao usuário
            report = await ReportService.get_report_by_id(report_id, user_id)
            
            # Excluir arquivo do Storage se existir
            if report.file_url:
                try:
                    # Extrair o caminho do arquivo do URL
                    file_path = report.file_url.split("/")[-1].split("?")[0]
                    blob = bucket.blob(f"reports/{file_path}")
                    blob.delete()
                except Exception as e:
                    print(f"Erro ao excluir arquivo do Storage: {str(e)}")
            
            # Excluir do Firestore
            db.collection("reports").document(report_id).delete()
            
            return {"message": "Relatório excluído com sucesso"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao excluir relatório: {str(e)}"
            )
    
    @staticmethod
    async def _generate_report_content(report_type: str, equipment_id: str, user_id: str) -> Dict[str, Any]:
        """Gera o conteúdo do relatório com base no tipo"""
        try:
            # Buscar dados do equipamento
            equipment_doc = db.collection("equipment").document(equipment_id).get()
            
            if not equipment_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Equipamento não encontrado"
                )
            
            equipment_data = equipment_doc.to_dict()
            
            # Gerar conteúdo com base no tipo de relatório
            if report_type == "health":
                return await ReportService._generate_health_report(equipment_data)
            elif report_type == "maintenance":
                return await ReportService._generate_maintenance_report(equipment_id, equipment_data)
            elif report_type == "prediction":
                return await ReportService._generate_prediction_report(equipment_data)
            elif report_type == "summary":
                return await ReportService._generate_summary_report(equipment_id, equipment_data, user_id)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Tipo de relatório inválido: {report_type}"
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao gerar conteúdo do relatório: {str(e)}"
            )
    
    @staticmethod
    async def _generate_health_report(equipment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera o conteúdo de um relatório de saúde do equipamento"""
        # Implementação simplificada - em um sistema real, usaria algoritmos mais complexos
        components_health = {}
        critical_components = []
        
        # Calcular saúde dos componentes
        for component in equipment_data.get("components", []):
            health = component.get("health_percentage", 0)
            components_health[component.get("name", "Componente desconhecido")] = health
            
            if health < 50:
                critical_components.append(component.get("name", "Componente desconhecido"))
        
        # Calcular saúde geral
        overall_health = 100
        if components_health:
            overall_health = sum(components_health.values()) / len(components_health)
        elif equipment_data.get("risk_level") == "high":
            overall_health = 30
        elif equipment_data.get("risk_level") == "medium":
            overall_health = 60
        
        # Gerar métricas operacionais
        operational_metrics = {
            "total_usage_hours": equipment_data.get("total_usage_hours", 0),
            "last_maintenance": equipment_data.get("last_maintenance_date", None),
            "next_maintenance": equipment_data.get("next_maintenance_date", None)
        }
        
        # Gerar recomendações
        recommendations = []
        if overall_health < 50:
            recommendations.append("Realizar manutenção preventiva urgente")
        if critical_components:
            recommendations.append(f"Verificar componentes críticos: {', '.join(critical_components)}")
        if equipment_data.get("total_usage_hours", 0) > 5000:
            recommendations.append("Considerar revisão geral devido ao alto tempo de uso")
        
        # Gerar tendência histórica (simplificada)
        historical_trend = []
        for i, data in enumerate(equipment_data.get("operational_data", [])[-5:]):
            historical_trend.append({
                "date": data.get("date", datetime.utcnow() - timedelta(days=30-i*5)),
                "health": max(0, min(100, overall_health - (5-i)*5))
            })
        
        return {
            "overall_health": overall_health,
            "risk_level": equipment_data.get("risk_level", "low"),
            "components_health": components_health,
            "critical_components": critical_components,
            "operational_metrics": operational_metrics,
            "recommendations": recommendations,
            "historical_trend": historical_trend
        }
    
    @staticmethod
    async def _generate_maintenance_report(equipment_id: str, equipment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera o conteúdo de um relatório de manutenção do equipamento"""
        # Buscar histórico de manutenções
        maintenance_docs = db.collection("maintenance").where("equipment_id", "==", equipment_id).order_by("created_at", direction=firestore.Query.DESCENDING).stream()
        
        maintenance_history = []
        components_replaced = []
        total_maintenance_cost = 0
        downtime_hours = 0
        
        for doc in maintenance_docs:
            maintenance_data = doc.to_dict()
            
            # Adicionar ao histórico
            maintenance_history.append({
                "id": maintenance_data.get("id"),
                "type": maintenance_data.get("maintenance_type"),
                "description": maintenance_data.get("description"),
                "status": maintenance_data.get("status"),
                "scheduled_date": maintenance_data.get("scheduled_date"),
                "completed_date": maintenance_data.get("completed_date"),
                "cost": maintenance_data.get("cost", 0)
            })
            
            # Somar custos e tempo de inatividade para manutenções concluídas
            if maintenance_data.get("status") == "completed":
                total_maintenance_cost += maintenance_data.get("cost", 0) or 0
                downtime_hours += maintenance_data.get("downtime_hours", 0) or 0
                
                # Adicionar componentes substituídos
                for component in maintenance_data.get("components_replaced", []) or []:
                    components_replaced.append({
                        "name": component,
                        "date": maintenance_data.get("completed_date"),
                        "maintenance_id": maintenance_data.get("id")
                    })
        
        # Calcular eficiência da manutenção (simplificado)
        maintenance_efficiency = None
        if len(maintenance_history) > 0:
            completed_count = sum(1 for m in maintenance_history if m["status"] == "completed")
            if completed_count > 0:
                # Eficiência baseada na redução do tempo de inatividade e custo ao longo do tempo
                maintenance_efficiency = max(0, min(100, 100 - (downtime_hours / completed_count) * 10))
        
        return {
            "last_maintenance_date": equipment_data.get("last_maintenance_date"),
            "next_maintenance_date": equipment_data.get("next_maintenance_date"),
            "maintenance_history": maintenance_history,
            "components_replaced": components_replaced,
            "total_maintenance_cost": total_maintenance_cost,
            "downtime_hours": downtime_hours,
            "maintenance_efficiency": maintenance_efficiency
        }
    
    @staticmethod
    async def _generate_prediction_report(equipment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera o conteúdo de um relatório de previsão para o equipamento"""
        # Implementação simplificada - em um sistema real, usaria modelos de ML mais complexos
        
        # Analisar dados operacionais
        operational_data = equipment_data.get("operational_data", [])
        data_points_analyzed = len(operational_data)
        
        # Previsões de falha (simplificadas)
        predicted_failures = []
        risk_factors = []
        estimated_lifetime = {}
        reliability_score = 85  # Valor padrão
        confidence_level = 70  # Valor padrão
        
        # Verificar componentes
        for component in equipment_data.get("components", []):
            component_name = component.get("name", "Componente desconhecido")
            health = component.get("health_percentage", 100)
            current_usage = component.get("current_usage_hours", 0)
            estimated_lifetime_hours = component.get("estimated_lifetime_hours", 10000)
            
            # Calcular tempo de vida restante
            remaining_hours = max(0, estimated_lifetime_hours - current_usage)
            remaining_percentage = (remaining_hours / estimated_lifetime_hours) * 100
            
            # Adicionar à estimativa de vida útil
            estimated_lifetime[component_name] = {
                "remaining_hours": remaining_hours,
                "remaining_percentage": remaining_percentage,
                "estimated_replacement_date": component.get("estimated_replacement_date")
            }
            
            # Verificar se o componente está em risco
            if health < 50 or remaining_percentage < 20:
                days_to_failure = int(remaining_hours / 8)  # Assumindo 8 horas de uso por dia
                
                predicted_failures.append({
                    "component": component_name,
                    "days_to_failure": days_to_failure,
                    "confidence": max(50, min(95, 100 - remaining_percentage)),
                    "recommended_action": "Substituir componente" if days_to_failure < 30 else "Monitorar de perto"
                })
                
                risk_factors.append({
                    "factor": f"Desgaste de {component_name}",
                    "impact": "Alto" if days_to_failure < 30 else "Médio",
                    "mitigation": "Substituição preventiva"
                })
        
        # Verificar tendências nos dados operacionais
        if len(operational_data) >= 3:
            # Verificar tendência de temperatura
            temp_trend = [d.get("temperature") for d in operational_data[-5:] if d.get("temperature") is not None]
            if temp_trend and len(temp_trend) >= 3 and temp_trend[-1] > temp_trend[0] * 1.2:
                predicted_failures.append({
                    "component": "Sistema de refrigeração",
                    "days_to_failure": 45,
                    "confidence": 75,
                    "recommended_action": "Verificar sistema de refrigeração"
                })
                
                risk_factors.append({
                    "factor": "Aumento de temperatura",
                    "impact": "Médio",
                    "mitigation": "Manutenção do sistema de refrigeração"
                })
            
            # Verificar tendência de vibração
            vibration_trend = [d.get("vibration") for d in operational_data[-5:] if d.get("vibration") is not None]
            if vibration_trend and len(vibration_trend) >= 3 and vibration_trend[-1] > vibration_trend[0] * 1.3:
                predicted_failures.append({
                    "component": "Sistema de transmissão",
                    "days_to_failure": 30,
                    "confidence": 80,
                    "recommended_action": "Verificar alinhamento e balanceamento"
                })
                
                risk_factors.append({
                    "factor": "Aumento de vibração",
                    "impact": "Alto",
                    "mitigation": "Alinhamento e balanceamento"
                })
        
        # Ajustar pontuação de confiabilidade com base nas previsões
        if predicted_failures:
            reliability_score = max(30, 100 - (len(predicted_failures) * 15))
            confidence_level = sum(f.get("confidence", 0) for f in predicted_failures) / len(predicted_failures)
        
        return {
            "predicted_failures": predicted_failures,
            "reliability_score": reliability_score,
            "estimated_lifetime_remaining": estimated_lifetime,
            "risk_factors": risk_factors,
            "confidence_level": confidence_level,
            "data_points_analyzed": data_points_analyzed
        }
    
    @staticmethod
    async def _generate_summary_report(equipment_id: str, equipment_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Gera um relatório resumido combinando informações de saúde, manutenção e previsão"""
        # Gerar relatórios individuais
        health_report = await ReportService._generate_health_report(equipment_data)
        maintenance_report = await ReportService._generate_maintenance_report(equipment_id, equipment_data)
        prediction_report = await ReportService._generate_prediction_report(equipment_data)
        
        # Buscar alertas recentes
        alerts_query = db.collection("alerts").where("equipment_id", "==", equipment_id).order_by("created_at", direction=firestore.Query.DESCENDING).limit(5).stream()
        
        recent_alerts = []
        for doc in alerts_query:
            alert_data = doc.to_dict()
            recent_alerts.append({
                "id": alert_data.get("id"),
                "message": alert_data.get("message"),
                "severity": alert_data.get("severity"),
                "status": alert_data.get("status"),
                "created_at": alert_data.get("created_at")
            })
        
        # Combinar em um relatório resumido
        return {
            "equipment_info": {
                "name": equipment_data.get("name"),
                "model": equipment_data.get("model"),
                "manufacturer": equipment_data.get("manufacturer"),
                "status": equipment_data.get("status"),
                "total_usage_hours": equipment_data.get("total_usage_hours", 0)
            },
            "health_summary": {
                "overall_health": health_report.get("overall_health"),
                "risk_level": health_report.get("risk_level"),
                "critical_components": health_report.get("critical_components")
            },
            "maintenance_summary": {
                "last_maintenance": maintenance_report.get("last_maintenance_date"),
                "next_maintenance": maintenance_report.get("next_maintenance_date"),
                "total_cost": maintenance_report.get("total_maintenance_cost"),
                "maintenance_count": len(maintenance_report.get("maintenance_history", []))
            },
            "prediction_summary": {
                "reliability_score": prediction_report.get("reliability_score"),
                "predicted_failures": prediction_report.get("predicted_failures"),
                "confidence_level": prediction_report.get("confidence_level")
            },
            "recent_alerts": recent_alerts,
            "recommendations": health_report.get("recommendations", []),
            "report_date": datetime.utcnow()
        }
    
    @staticmethod
    async def _generate_pdf(report_id: str, report_data: Dict[str, Any]) -> Optional[str]:
        """Gera um arquivo PDF do relatório e salva no Storage"""
        try:
            # Implementação simplificada - em um sistema real, usaria uma biblioteca como WeasyPrint
            # para gerar um PDF real a partir de um template HTML
            
            # Criar nome do arquivo
            file_name = f"{report_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.pdf"
            
            # Caminho no Storage
            storage_path = f"reports/{file_name}"
            
            # Em um sistema real, aqui geraria o PDF e o salvaria temporariamente
            # Depois faria upload para o Storage
            
            # Simular URL do arquivo
            file_url = f"https://storage.googleapis.com/{bucket.name}/{storage_path}"
            
            return file_url
        except Exception as e:
            print(f"Erro ao gerar PDF: {str(e)}")
            return None