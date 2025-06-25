from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import uuid

from fastapi import HTTPException, status
from firebase_admin import firestore

from config import db
from models.maintenance import Maintenance, MaintenanceCreate, MaintenanceUpdate

class MaintenanceService:
    @staticmethod
    async def create_maintenance(user_id: str, maintenance_data: MaintenanceCreate) -> Maintenance:
        try:
            # Gerar ID único para a manutenção
            maintenance_id = str(uuid.uuid4())
            
            # Buscar nome do equipamento
            equipment_doc = db.collection("equipment").document(maintenance_data.equipment_id).get()
            
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
            
            # Preparar dados da manutenção
            maintenance_dict = maintenance_data.dict()
            maintenance_dict.update({
                "id": maintenance_id,
                "user_id": user_id,
                "equipment_name": equipment_name,
                "status": "scheduled",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            
            # Adicionar ao Firestore
            db.collection("maintenance").document(maintenance_id).set(maintenance_dict)
            
            # Atualizar status do equipamento se necessário
            if equipment_data.get("needs_maintenance", False):
                db.collection("equipment").document(maintenance_data.equipment_id).update({
                    "status": "maintenance",
                    "updated_at": datetime.utcnow()
                })
            
            return Maintenance(**maintenance_dict)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao criar registro de manutenção: {str(e)}"
            )
    
    @staticmethod
    async def get_maintenance_by_id(maintenance_id: str, user_id: str) -> Maintenance:
        try:
            maintenance_doc = db.collection("maintenance").document(maintenance_id).get()
            
            if not maintenance_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro de manutenção não encontrado"
                )
            
            maintenance_data = maintenance_doc.to_dict()
            
            # Verificar se a manutenção pertence ao usuário
            if maintenance_data["user_id"] != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Acesso não autorizado a este registro de manutenção"
                )
            
            return Maintenance(**maintenance_data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao buscar registro de manutenção: {str(e)}"
            )
    
    @staticmethod
    async def get_all_maintenance(user_id: str, equipment_id: Optional[str] = None, status: Optional[str] = None) -> List[Maintenance]:
        try:
            # Iniciar consulta base
            query = db.collection("maintenance").where("user_id", "==", user_id)
            
            # Adicionar filtro de equipamento se fornecido
            if equipment_id:
                query = query.where("equipment_id", "==", equipment_id)
            
            # Adicionar filtro de status se fornecido
            if status:
                query = query.where("status", "==", status)
            
            # Ordenar por data agendada (mais próximas primeiro)
            query = query.order_by("scheduled_date", direction=firestore.Query.ASCENDING)
            
            # Executar consulta
            maintenance_docs = query.stream()
            
            maintenance_list = []
            for doc in maintenance_docs:
                maintenance_data = doc.to_dict()
                maintenance_list.append(Maintenance(**maintenance_data))
            
            return maintenance_list
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao listar registros de manutenção: {str(e)}"
            )
    
    @staticmethod
    async def update_maintenance(maintenance_id: str, user_id: str, maintenance_data: MaintenanceUpdate) -> Maintenance:
        try:
            # Verificar se a manutenção existe e pertence ao usuário
            maintenance = await MaintenanceService.get_maintenance_by_id(maintenance_id, user_id)
            
            # Preparar dados para atualização
            update_data = maintenance_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            # Verificar se o status está sendo alterado para "completed"
            status_changed_to_completed = update_data.get("status") == "completed" and maintenance.status != "completed"
            
            # Atualizar no Firestore
            db.collection("maintenance").document(maintenance_id).update(update_data)
            
            # Se a manutenção foi concluída, atualizar o equipamento
            if status_changed_to_completed:
                # Buscar equipamento
                equipment_doc = db.collection("equipment").document(maintenance.equipment_id).get()
                
                if equipment_doc.exists:
                    # Atualizar status do equipamento
                    db.collection("equipment").document(maintenance.equipment_id).update({
                        "status": "active",
                        "needs_maintenance": False,
                        "risk_level": "low",
                        "last_maintenance_date": datetime.utcnow(),
                        "next_maintenance_date": datetime.utcnow() + timedelta(days=90),  # Valor padrão
                        "updated_at": datetime.utcnow()
                    })
                    
                    # Resolver alertas ativos para este equipamento
                    alerts_query = db.collection("alerts").where("equipment_id", "==", maintenance.equipment_id).where("status", "==", "active").stream()
                    
                    for alert_doc in alerts_query:
                        db.collection("alerts").document(alert_doc.id).update({
                            "status": "resolved",
                            "resolved_at": datetime.utcnow(),
                            "resolution_notes": "Resolvido automaticamente após manutenção concluída.",
                            "updated_at": datetime.utcnow()
                        })
            
            # Buscar manutenção atualizada
            updated_maintenance = await MaintenanceService.get_maintenance_by_id(maintenance_id, user_id)
            return updated_maintenance
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao atualizar registro de manutenção: {str(e)}"
            )
    
    @staticmethod
    async def delete_maintenance(maintenance_id: str, user_id: str) -> Dict[str, str]:
        try:
            # Verificar se a manutenção existe e pertence ao usuário
            maintenance = await MaintenanceService.get_maintenance_by_id(maintenance_id, user_id)
            
            # Excluir do Firestore
            db.collection("maintenance").document(maintenance_id).delete()
            
            return {"message": "Registro de manutenção excluído com sucesso"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao excluir registro de manutenção: {str(e)}"
            )
    
    @staticmethod
    async def schedule_maintenance_for_equipment(equipment_id: str, user_id: str, days_ahead: int = 7) -> Maintenance:
        """Agenda uma manutenção automática para um equipamento com base na análise de risco"""
        try:
            # Buscar informações do equipamento
            equipment_doc = db.collection("equipment").document(equipment_id).get()
            
            if not equipment_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Equipamento não encontrado"
                )
            
            equipment_data = equipment_doc.to_dict()
            equipment_name = equipment_data.get("name", "Equipamento desconhecido")
            
            # Verificar se já existe uma manutenção agendada para este equipamento
            existing_maintenance = db.collection("maintenance").where("equipment_id", "==", equipment_id).where("status", "in", ["scheduled", "in_progress"]).limit(1).stream()
            
            for _ in existing_maintenance:
                # Já existe uma manutenção agendada, não criar outra
                return
            
            # Criar dados da manutenção
            maintenance_id = str(uuid.uuid4())
            scheduled_date = datetime.utcnow() + timedelta(days=days_ahead)
            
            maintenance_dict = {
                "id": maintenance_id,
                "user_id": user_id,
                "equipment_id": equipment_id,
                "equipment_name": equipment_name,
                "maintenance_type": "preventive",
                "description": f"Manutenção preventiva automática para {equipment_name} devido a risco elevado.",
                "status": "scheduled",
                "scheduled_date": scheduled_date,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Adicionar ao Firestore
            db.collection("maintenance").document(maintenance_id).set(maintenance_dict)
            
            return Maintenance(**maintenance_dict)
        except Exception as e:
            print(f"Erro ao agendar manutenção automática: {str(e)}")
            # Não propagar exceção para não interromper o fluxo principal