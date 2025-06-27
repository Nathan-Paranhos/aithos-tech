from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid
import os
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client

from fastapi import HTTPException, status
from firebase_admin import firestore

from config import db
from models.alert import Alert, AlertCreate, AlertUpdate

class AlertService:
    @staticmethod
    async def create_alert(user_id: str, alert_data: AlertCreate) -> Alert:
        try:
            alert_id = str(uuid.uuid4())
            equipment_doc = db.collection("equipment").document(alert_data.equipment_id).get()
            if not equipment_doc.exists:
                raise HTTPException(status_code=404, detail="Equipamento não encontrado")
            
            equipment_data = equipment_doc.to_dict()
            if equipment_data["user_id"] != user_id:
                raise HTTPException(status_code=403, detail="Acesso não autorizado a este equipamento")
            
            alert_dict = alert_data.dict()
            alert_dict.update({
                "id": alert_id,
                "user_id": user_id,
                "equipment_name": equipment_data.get("name", "Equipamento desconhecido"),
                "status": "active",
                "updated_at": datetime.utcnow(),
                "notification_sent": False
            })

            db.collection("alerts").document(alert_id).set(alert_dict)
            await AlertService._send_notification(alert_dict)

            return Alert(**alert_dict)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def create_alert_for_equipment(equipment_id: str, user_id: str) -> Optional[Alert]:
        try:
            equipment_doc = db.collection("equipment").document(equipment_id).get()
            if not equipment_doc.exists:
                raise HTTPException(status_code=404, detail="Equipamento não encontrado")
            
            equipment_data = equipment_doc.to_dict()
            equipment_name = equipment_data.get("name", "Equipamento desconhecido")
            
            existing_alerts = db.collection("alerts")\
                .where("equipment_id", "==", equipment_id)\
                .where("status", "==", "active")\
                .limit(1).stream()
            
            for _ in existing_alerts:
                return  # já existe alerta ativo

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
                "predicted_failure_days": None,
                "recommended_action": "Verificar sensores e realizar manutenção preventiva.",
                "notification_sent": False
            }

            db.collection("alerts").document(alert_id).set(alert_dict)
            await AlertService._send_notification(alert_dict)

            return Alert(**alert_dict)
        except Exception as e:
            print(f"Erro ao criar alerta automático: {str(e)}")

    @staticmethod
    async def get_alert_by_id(alert_id: str, user_id: str) -> Alert:
        try:
            alert_doc = db.collection("alerts").document(alert_id).get()
            if not alert_doc.exists:
                raise HTTPException(status_code=404, detail="Alerta não encontrado")
            
            alert_data = alert_doc.to_dict()
            if alert_data["user_id"] != user_id:
                raise HTTPException(status_code=403, detail="Acesso não autorizado")
            
            return Alert(**alert_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_all_alerts(user_id: str, status: Optional[str] = None) -> List[Alert]:
        try:
            query = db.collection("alerts").where("user_id", "==", user_id)
            if status:
                query = query.where("status", "==", status)
            query = query.order_by("created_at", direction=firestore.Query.DESCENDING)
            alert_docs = query.stream()
            return [Alert(**doc.to_dict()) for doc in alert_docs]
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def update_alert(alert_id: str, user_id: str, alert_data: AlertUpdate) -> Alert:
        try:
            alert = await AlertService.get_alert_by_id(alert_id, user_id)
            update_data = alert_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            if "status" in update_data:
                if update_data["status"] == "acknowledged" and not alert.acknowledged_at:
                    update_data["acknowledged_at"] = datetime.utcnow()
                elif update_data["status"] == "resolved" and not alert.resolved_at:
                    update_data["resolved_at"] = datetime.utcnow()

            db.collection("alerts").document(alert_id).update(update_data)
            return await AlertService.get_alert_by_id(alert_id, user_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def delete_alert(alert_id: str, user_id: str) -> Dict[str, str]:
        try:
            await AlertService.get_alert_by_id(alert_id, user_id)
            db.collection("alerts").document(alert_id).delete()
            return {"message": "Alerta excluído com sucesso"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def _send_notification(alert_data: Dict[str, Any]) -> None:
        try:
            user_doc = db.collection("users").document(alert_data["user_id"]).get()
            if not user_doc.exists:
                return
            user_data = user_doc.to_dict()

            # mensagem
            message = f"Alerta AgroGuard para {alert_data.get('equipment_name')}: {alert_data.get('message')}. Severidade: {alert_data.get('severity')}. Ação recomendada: {alert_data.get('recommended_action')}"

            # Email
            if os.getenv("EMAIL_USERNAME") and os.getenv("EMAIL_PASSWORD") and user_data.get("email"):
                try:
                    msg = MIMEText(message)
                    msg["Subject"] = f"Alerta AgroGuard: {alert_data.get('equipment_name')}"
                    msg["From"] = os.getenv("EMAIL_USERNAME")
                    msg["To"] = user_data.get("email")
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                        smtp.login(os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD"))
                        smtp.send_message(msg)
                    print(f"E-mail enviado para {user_data.get('email')}")
                except Exception as e:
                    print(f"Erro ao enviar e-mail: {e}")

            # SMS
            if os.getenv("TWILIO_ACCOUNT_SID") and os.getenv("TWILIO_AUTH_TOKEN") and os.getenv("TWILIO_PHONE_NUMBER") and user_data.get("phone_number"):
                try:
                    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
                    client.messages.create(
                        to=user_data.get("phone_number"),
                        from_=os.getenv("TWILIO_PHONE_NUMBER"),
                        body=message
                    )
                    print(f"SMS enviado para {user_data.get('phone_number')}")
                except Exception as e:
                    print(f"Erro ao enviar SMS: {e}")

            # Atualizar status no Firestore
            db.collection("alerts").document(alert_data["id"]).update({
                "notification_sent": True,
                "notification_sent_at": datetime.utcnow()
            })

        except Exception as e:
            print(f"Erro geral no envio de notificação: {str(e)}")
