from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid
import os
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
from datetime import datetime

from fastapi import HTTPException, status
from firebase_admin import firestore

from config import db
from models.alert import Alert, AlertCreate, AlertUpdate

class AlertService:
    @staticmethod
    async def create_alert(user_id: str, alert_data: AlertCreate) -> Alert:
        try:
            # Gerar ID único para o alerta
            alert_id = str(uuid.uuid4())
            
            # Buscar nome do equipamento
            equipment_doc = db.collection("equipment").document(alert_data.equipment_id).get()
            
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
            
            # Preparar dados do alerta
            alert_dict = alert_data.dict()
            alert_dict.update({
                "id": alert_id,
                "user_id": user_id,
                "equipment_name": equipment_name,
                "status": "active",

                "updated_at": datetime.utcnow(),
                "notification_sent": False
            })
            
            # Adicionar ao Firestore
            db.collection("alerts").document(alert_id).set(alert_dict)
            
            # Enviar notificação (implementação simplificada)
            await AlertService._send_notification(alert_dict)
            
            return Alert(**alert_dict)

    @staticmethod
    async def _send_notification(alert_data: Dict[str, Any]):
        """Envia notificações por e-mail e SMS"""
        user_id = alert_data.get("user_id")
        if not user_id:
            print("User ID not found for alert, cannot send notification.")
            return

        user_doc = db.collection("users").document(user_id).get()
        if not user_doc.exists:
            print(f"User with ID {user_id} not found, cannot send notification.")
            return
        user_data = user_doc.to_dict()
        user_email = user_data.get("email")
        user_phone = user_data.get("phone_number")

        alert_message = f"Alerta AgroGuard para {alert_data.get('equipment_name')}: {alert_data.get('message')}. Severidade: {alert_data.get('severity')}. Ação recomendada: {alert_data.get('recommended_action')}"

        # Envio por E-mail
        if user_email and os.getenv("EMAIL_USERNAME") and os.getenv("EMAIL_PASSWORD"):
            try:
                msg = MIMEText(alert_message)
                msg["Subject"] = f"Alerta AgroGuard: {alert_data.get('equipment_name')}"
                msg["From"] = os.getenv("EMAIL_USERNAME")
                msg["To"] = user_email

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD"))
                    smtp.send_message(msg)
                print(f"Email de alerta enviado para {user_email}")
            except Exception as e:
                print(f"Erro ao enviar email de alerta: {e}")
        else:
            print("Configurações de email incompletas ou email do usuário não disponível.")

        # Envio por SMS (Twilio)
        if user_phone and os.getenv("TWILIO_ACCOUNT_SID") and os.getenv("TWILIO_AUTH_TOKEN") and os.getenv("TWILIO_PHONE_NUMBER"):
            try:
                client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
                client.messages.create(
                    to=user_phone,
                    from_=os.getenv("TWILIO_PHONE_NUMBER"),
                    body=alert_message
                )
                print(f"SMS de alerta enviado para {user_phone}")
            except Exception as e:
                print(f"Erro ao enviar SMS de alerta: {e}")
        else:
            print("Configurações do Twilio incompletas ou telefone do usuário não disponível.")



    
    @staticmethod
    async def create_alert_for_equipment(equipment_id: str, user_id: str) -> Alert:
        """Cria um alerta automático para um equipamento com base na análise de saúde"""
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
            
            # Verificar se já existe um alerta ativo para este equipamento
            existing_alerts = db.collection("alerts").where("equipment_id", "==", equipment_id).where("status", "==", "active").limit(1).stream()
            
            for _ in existing_alerts:
                # Já existe um alerta ativo, não criar outro
                return
            
            # Criar dados do alerta
            alert_id = str(uuid.uuid4())
            alert_dict = {
                "id": alert_id,
                "user_id": user_id,
                "equipment_id": equipment_id,
                "equipment_name": equipment_name,
                "message": f"Risco elevado detectado para {equipment_name}. Manutenção recomendada.",
                "severity": "high",
                "status": "active",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "predicted_failure_days": None, # Será preenchido pela IA
                "recommended_action": "Verificar sensores e realizar manutenção preventiva.", # Será preenchido pela IA
                "notification_sent": False
            }

            # Adicionar ao Firestore
            db.collection("alerts").document(alert_id).set(alert_dict)

            # Enviar notificação
            await AlertService._send_notification(alert_dict)

            return Alert(**alert_dict)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao criar alerta para equipamento: {str(e)}"
            )
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "notification_sent": False
            }
            
            # Adicionar ao Firestore
            db.collection("alerts").document(alert_id).set(alert_dict)
            
            # Enviar notificação
            await AlertService._send_notification(alert_dict)
            
            return Alert(**alert_dict)
        except Exception as e:
            print(f"Erro ao criar alerta automático: {str(e)}")
            # Não propagar exceção para não interromper o fluxo principal
    
    @staticmethod
    async def get_alert_by_id(alert_id: str, user_id: str) -> Alert:
        try:
            alert_doc = db.collection("alerts").document(alert_id).get()
            
            if not alert_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Alerta não encontrado"
                )
            
            alert_data = alert_doc.to_dict()
            
            # Verificar se o alerta pertence ao usuário
            if alert_data["user_id"] != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Acesso não autorizado a este alerta"
                )
            
            return Alert(**alert_data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao buscar alerta: {str(e)}"
            )
    
    @staticmethod
    async def get_all_alerts(user_id: str, status: Optional[str] = None) -> List[Alert]:
        try:
            # Iniciar consulta base
            query = db.collection("alerts").where("user_id", "==", user_id)
            
            # Adicionar filtro de status se fornecido
            if status:
                query = query.where("status", "==", status)
            
            # Ordenar por data de criação (mais recentes primeiro)
            query = query.order_by("created_at", direction=firestore.Query.DESCENDING)
            
            # Executar consulta
            alert_docs = query.stream()
            
            alert_list = []
            for doc in alert_docs:
                alert_data = doc.to_dict()
                alert_list.append(Alert(**alert_data))
            
            return alert_list
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao listar alertas: {str(e)}"
            )
    
    @staticmethod
    async def update_alert(alert_id: str, user_id: str, alert_data: AlertUpdate) -> Alert:
        try:
            # Verificar se o alerta existe e pertence ao usuário
            alert = await AlertService.get_alert_by_id(alert_id, user_id)
            
            # Preparar dados para atualização
            update_data = alert_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            # Adicionar timestamps específicos com base no status
            if "status" in update_data:
                if update_data["status"] == "acknowledged" and not alert.acknowledged_at:
                    update_data["acknowledged_at"] = datetime.utcnow()
                elif update_data["status"] == "resolved" and not alert.resolved_at:
                    update_data["resolved_at"] = datetime.utcnow()
            
            # Atualizar no Firestore
            db.collection("alerts").document(alert_id).update(update_data)
            
            # Buscar alerta atualizado
            updated_alert = await AlertService.get_alert_by_id(alert_id, user_id)
            return updated_alert
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao atualizar alerta: {str(e)}"
            )
    
    @staticmethod
    async def delete_alert(alert_id: str, user_id: str) -> Dict[str, str]:
        try:
            # Verificar se o alerta existe e pertence ao usuário
            alert = await AlertService.get_alert_by_id(alert_id, user_id)
            
            # Excluir do Firestore
            db.collection("alerts").document(alert_id).delete()
            
            return {"message": "Alerta excluído com sucesso"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao excluir alerta: {str(e)}"
            )
    
    @staticmethod
    async def _send_notification(alert_data: Dict[str, Any]) -> None:
        """Envia notificações para o usuário com base nas preferências"""
        try:
            # Buscar preferências de notificação do usuário
            user_doc = db.collection("users").document(alert_data["user_id"]).get()
            
            if not user_doc.exists:
                return
            
            user_data = user_doc.to_dict()
            notification_prefs = user_data.get("notification_preferences", {})
            
            # Verificar se deve enviar notificação apenas para alertas de alto risco
            if notification_prefs.get("high_risk_only", False) and alert_data.get("severity") != "high":
                return
            
            # Marcar notificação como enviada
            db.collection("alerts").document(alert_data["id"]).update({
                "notification_sent": True,
                "notification_sent_at": datetime.utcnow()
            })
            
            # Implementação simplificada - em um sistema real, enviaria emails e mensagens
            # Aqui apenas registramos que a notificação seria enviada
            print(f"Notificação enviada para {user_data.get('email')} sobre alerta {alert_data['id']}")
            
        except Exception as e:
            print(f"Erro ao enviar notificação: {str(e)}")
            # Não propagar exceção para não interromper o fluxo principal