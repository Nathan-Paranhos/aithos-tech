from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import uuid

from fastapi import HTTPException, status

from config import db
from models.equipment import Equipment, EquipmentCreate, EquipmentUpdate, OperationalData

class EquipmentService:
    @staticmethod
    async def create_equipment(user_id: str, equipment_data: EquipmentCreate) -> Equipment:
        try:
            # Gerar ID único para o equipamento
            equipment_id = str(uuid.uuid4())
            
            # Preparar dados do equipamento
            equipment_dict = equipment_data.dict()
            equipment_dict.update({
                "id": equipment_id,
                "user_id": user_id,
                "status": "active",
                "risk_level": "low",
                "needs_maintenance": False,
                "components": [],
                "operational_data": [],
                "total_usage_hours": 0,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            
            # Adicionar ao Firestore
            db.collection("equipment").document(equipment_id).set(equipment_dict)
            
            return Equipment(**equipment_dict)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao criar equipamento: {str(e)}"
            )
    
    @staticmethod
    async def get_equipment_by_id(equipment_id: str, user_id: str) -> Equipment:
        try:
            equipment_doc = db.collection("equipment").document(equipment_id).get()
            
            if not equipment_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Equipamento não encontrado"
                )
            
            equipment_data = equipment_doc.to_dict()
            
            # Verificar se o equipamento pertence ao usuário
            if equipment_data["user_id"] != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Acesso não autorizado a este equipamento"
                )
            
            return Equipment(**equipment_data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao buscar equipamento: {str(e)}"
            )
    
    @staticmethod
    async def get_all_equipment(user_id: str) -> List[Equipment]:
        try:
            equipment_docs = db.collection("equipment").where("user_id", "==", user_id).stream()
            
            equipment_list = []
            for doc in equipment_docs:
                equipment_data = doc.to_dict()
                equipment_list.append(Equipment(**equipment_data))
            
            return equipment_list
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao listar equipamentos: {str(e)}"
            )
    
    @staticmethod
    async def update_equipment(equipment_id: str, user_id: str, equipment_data: EquipmentUpdate) -> Equipment:
        try:
            # Verificar se o equipamento existe e pertence ao usuário
            equipment = await EquipmentService.get_equipment_by_id(equipment_id, user_id)
            
            # Preparar dados para atualização
            update_data = equipment_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            # Atualizar no Firestore
            db.collection("equipment").document(equipment_id).update(update_data)
            
            # Buscar equipamento atualizado
            updated_equipment = await EquipmentService.get_equipment_by_id(equipment_id, user_id)
            return updated_equipment
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao atualizar equipamento: {str(e)}"
            )
    
    @staticmethod
    async def delete_equipment(equipment_id: str, user_id: str) -> Dict[str, str]:
        try:
            # Verificar se o equipamento existe e pertence ao usuário
            equipment = await EquipmentService.get_equipment_by_id(equipment_id, user_id)
            
            # Excluir do Firestore
            db.collection("equipment").document(equipment_id).delete()
            
            return {"message": "Equipamento excluído com sucesso"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao excluir equipamento: {str(e)}"
            )
    
    @staticmethod
    async def add_operational_data(equipment_id: str, user_id: str, data: OperationalData) -> Equipment:
        try:
            # Verificar se o equipamento existe e pertence ao usuário
            equipment = await EquipmentService.get_equipment_by_id(equipment_id, user_id)
            
            # Adicionar dados operacionais
            operational_data = data.dict()
            
            # Atualizar no Firestore usando arrayUnion para adicionar ao array
            db.collection("equipment").document(equipment_id).update({
                "operational_data": firestore.ArrayUnion([operational_data]),
                "total_usage_hours": equipment.total_usage_hours + data.hours_used,
                "updated_at": datetime.utcnow()
            })
            
            # Analisar dados e atualizar status de risco se necessário
            await EquipmentService._analyze_equipment_health(equipment_id, user_id)
            
            # Buscar equipamento atualizado
            updated_equipment = await EquipmentService.get_equipment_by_id(equipment_id, user_id)
            return updated_equipment
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao adicionar dados operacionais: {str(e)}"
            )
    
    @staticmethod
    async def _analyze_equipment_health(equipment_id: str, user_id: str) -> None:
        """Analisa a saúde do equipamento com base nos dados operacionais e atualiza o nível de risco"""
        try:
            # Buscar equipamento
            equipment = await EquipmentService.get_equipment_by_id(equipment_id, user_id)
            
            # Implementação simplificada de análise
            # Em um sistema real, isso usaria algoritmos de ML mais complexos
            if len(equipment.operational_data) < 3:
                return  # Dados insuficientes para análise
            
            # Ordenar dados por data
            sorted_data = sorted(equipment.operational_data, key=lambda x: x.date)
            recent_data = sorted_data[-3:]  # Últimos 3 registros
            
            # Verificar tendências de temperatura e vibração
            temp_trend = [d.temperature for d in recent_data if d.temperature is not None]
            vibration_trend = [d.vibration for d in recent_data if d.vibration is not None]
            
            risk_level = "low"
            needs_maintenance = False
            
            # Lógica simplificada de análise
            if temp_trend and len(temp_trend) >= 3:
                if temp_trend[-1] > 80 or (temp_trend[-1] > temp_trend[-2] > temp_trend[-3] and temp_trend[-1] > 70):
                    risk_level = "high"
                    needs_maintenance = True
                elif temp_trend[-1] > 60:
                    risk_level = "medium"
            
            if vibration_trend and len(vibration_trend) >= 3:
                if vibration_trend[-1] > 0.8 or (vibration_trend[-1] > vibration_trend[-2] > vibration_trend[-3] and vibration_trend[-1] > 0.6):
                    risk_level = "high"
                    needs_maintenance = True
                elif vibration_trend[-1] > 0.5:
                    risk_level = "medium"
            
            # Atualizar equipamento se o risco mudou
            if risk_level != equipment.risk_level or needs_maintenance != equipment.needs_maintenance:
                db.collection("equipment").document(equipment_id).update({
                    "risk_level": risk_level,
                    "needs_maintenance": needs_maintenance,
                    "updated_at": datetime.utcnow()
                })
                
                # Se o risco for alto, criar um alerta
                if risk_level == "high":
                    from services.alert_service import AlertService
                    await AlertService.create_alert_for_equipment(equipment_id, user_id)
                    
        except Exception as e:
            print(f"Erro ao analisar saúde do equipamento: {str(e)}")
            # Não propagar exceção para não interromper o fluxo principal