from typing import Dict, Any, List, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from fastapi import HTTPException, status

from config import settings

class EmailSender:
    """Classe para envio de emails"""
    
    @staticmethod
    async def send_email(to_email: str, subject: str, html_content: str) -> bool:
        """Envia um email usando SMTP"""
        try:
            # Configurar mensagem
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = settings.EMAIL_FROM
            message["To"] = to_email
            
            # Adicionar conteúdo HTML
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Conectar ao servidor SMTP
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
                server.sendmail(settings.EMAIL_FROM, to_email, message.as_string())
            
            return True
        except Exception as e:
            print(f"Erro ao enviar email: {str(e)}")
            return False
    
    @staticmethod
    async def send_alert_notification(to_email: str, alert_data: Dict[str, Any]) -> bool:
        """Envia uma notificação de alerta por email"""
        # Determinar cor com base na severidade
        severity = alert_data.get("severity", "medium")
        if severity == "high":
            color = "#FF4136"  # Vermelho
        elif severity == "medium":
            color = "#FF851B"  # Laranja
        else:
            color = "#2ECC40"  # Verde
        
        # Construir conteúdo HTML
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .alert {{ padding: 20px; border-radius: 5px; background-color: #f8f9fa; border-left: 5px solid {color}; }}
                .header {{ color: {color}; font-weight: bold; font-size: 18px; }}
                .details {{ margin-top: 15px; }}
                .action {{ margin-top: 20px; }}
                .button {{ background-color: #0074D9; color: white; padding: 10px 15px; text-decoration: none; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="alert">
                <div class="header">Alerta: {alert_data.get('message', 'Novo alerta detectado')}</div>
                <div class="details">
                    <p><strong>Equipamento:</strong> {alert_data.get('equipment_name', 'Não especificado')}</p>
                    <p><strong>Severidade:</strong> {severity.upper()}</p>
                    <p><strong>Componente:</strong> {alert_data.get('component', 'Não especificado')}</p>
                    <p><strong>Dias previstos até falha:</strong> {alert_data.get('predicted_failure_days', 'Não especificado')}</p>
                    <p><strong>Ação recomendada:</strong> {alert_data.get('recommended_action', 'Verificar equipamento')}</p>
                </div>
                <div class="action">
                    <a href="http://localhost:3000/alerts/{alert_data.get('id', '')}" class="button">Ver Detalhes</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await EmailSender.send_email(
            to_email,
            f"Alerta AgroGuard: {alert_data.get('message', 'Novo alerta detectado')}",
            html_content
        )
    
    @staticmethod
    async def send_maintenance_reminder(to_email: str, maintenance_data: Dict[str, Any]) -> bool:
        """Envia um lembrete de manutenção por email"""
        # Construir conteúdo HTML
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .reminder {{ padding: 20px; border-radius: 5px; background-color: #f8f9fa; border-left: 5px solid #0074D9; }}
                .header {{ color: #0074D9; font-weight: bold; font-size: 18px; }}
                .details {{ margin-top: 15px; }}
                .action {{ margin-top: 20px; }}
                .button {{ background-color: #0074D9; color: white; padding: 10px 15px; text-decoration: none; border-radius: 3px; }}
                .date {{ font-weight: bold; color: #FF4136; }}
            </style>
        </head>
        <body>
            <div class="reminder">
                <div class="header">Lembrete de Manutenção Agendada</div>
                <div class="details">
                    <p><strong>Equipamento:</strong> {maintenance_data.get('equipment_name', 'Não especificado')}</p>
                    <p><strong>Tipo de Manutenção:</strong> {maintenance_data.get('maintenance_type', 'Preventiva').upper()}</p>
                    <p><strong>Data Agendada:</strong> <span class="date">{maintenance_data.get('scheduled_date', 'Não especificada')}</span></p>
                    <p><strong>Descrição:</strong> {maintenance_data.get('description', 'Manutenção regular')}</p>
                </div>
                <div class="action">
                    <a href="http://localhost:3000/maintenance/{maintenance_data.get('id', '')}" class="button">Ver Detalhes</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await EmailSender.send_email(
            to_email,
            f"Lembrete de Manutenção AgroGuard: {maintenance_data.get('equipment_name', 'Equipamento')}",
            html_content
        )
    
    @staticmethod
    async def send_report_notification(to_email: str, report_data: Dict[str, Any]) -> bool:
        """Envia uma notificação de relatório por email"""
        # Construir conteúdo HTML
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .report {{ padding: 20px; border-radius: 5px; background-color: #f8f9fa; border-left: 5px solid #2ECC40; }}
                .header {{ color: #2ECC40; font-weight: bold; font-size: 18px; }}
                .details {{ margin-top: 15px; }}
                .action {{ margin-top: 20px; }}
                .button {{ background-color: #0074D9; color: white; padding: 10px 15px; text-decoration: none; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="report">
                <div class="header">Novo Relatório Disponível</div>
                <div class="details">
                    <p><strong>Título:</strong> {report_data.get('title', 'Relatório')}</p>
                    <p><strong>Tipo:</strong> {report_data.get('report_type', 'Não especificado').upper()}</p>
                    <p><strong>Equipamento:</strong> {report_data.get('equipment_name', 'Não especificado')}</p>
                    <p><strong>Data de Geração:</strong> {report_data.get('created_at', 'Não especificada')}</p>
                </div>
                <div class="action">
                    <a href="http://localhost:3000/reports/{report_data.get('id', '')}" class="button">Ver Relatório</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await EmailSender.send_email(
            to_email,
            f"Novo Relatório AgroGuard: {report_data.get('title', 'Relatório')}",
            html_content
        )

class SMSSender:
    """Classe para envio de SMS usando Twilio"""
    
    @staticmethod
    async def send_sms(to_phone: str, message: str) -> bool:
        """Envia um SMS usando a API do Twilio"""
        try:
            # Inicializar cliente Twilio
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            # Enviar mensagem
            message = client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=to_phone
            )
            
            return True
        except Exception as e:
            print(f"Erro ao enviar SMS: {str(e)}")
            return False
    
    @staticmethod
    async def send_alert_sms(to_phone: str, alert_data: Dict[str, Any]) -> bool:
        """Envia uma notificação de alerta por SMS"""
        message = f"ALERTA AgroGuard: {alert_data.get('message', 'Novo alerta')}. "
        message += f"Equipamento: {alert_data.get('equipment_name', 'Não especificado')}. "
        message += f"Severidade: {alert_data.get('severity', 'média').upper()}. "
        message += f"Ação: {alert_data.get('recommended_action', 'Verificar equipamento')}"
        
        return await SMSSender.send_sms(to_phone, message)
    
    @staticmethod
    async def send_maintenance_sms(to_phone: str, maintenance_data: Dict[str, Any]) -> bool:
        """Envia um lembrete de manutenção por SMS"""
        message = f"Lembrete de Manutenção AgroGuard: {maintenance_data.get('equipment_name', 'Equipamento')}. "
        message += f"Tipo: {maintenance_data.get('maintenance_type', 'Preventiva').upper()}. "
        message += f"Data: {maintenance_data.get('scheduled_date', 'Não especificada')}"
        
        return await SMSSender.send_sms(to_phone, message)

class NotificationManager:
    """Gerenciador de notificações que coordena diferentes canais"""
    
    @staticmethod
    async def send_notification(user_data: Dict[str, Any], notification_type: str, data: Dict[str, Any]) -> Dict[str, bool]:
        """Envia notificações pelos canais configurados pelo usuário"""
        results = {}
        notification_prefs = user_data.get("notification_preferences", {})
        
        # Verificar preferências de email
        if notification_prefs.get("email", True) and user_data.get("email"):
            if notification_type == "alert":
                results["email"] = await EmailSender.send_alert_notification(user_data["email"], data)
            elif notification_type == "maintenance":
                results["email"] = await EmailSender.send_maintenance_reminder(user_data["email"], data)
            elif notification_type == "report":
                results["email"] = await EmailSender.send_report_notification(user_data["email"], data)
        
        # Verificar preferências de SMS
        if notification_prefs.get("sms", False) and user_data.get("phone_number"):
            if notification_type == "alert":
                results["sms"] = await SMSSender.send_alert_sms(user_data["phone_number"], data)
            elif notification_type == "maintenance":
                results["sms"] = await SMSSender.send_maintenance_sms(user_data["phone_number"], data)
        
        return results