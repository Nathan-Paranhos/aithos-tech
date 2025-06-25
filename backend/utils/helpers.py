from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
import re
import uuid
import math
import json
from fastapi import HTTPException, status

def generate_id() -> str:
    """Gera um ID único para uso em documentos"""
    return str(uuid.uuid4())

def format_timestamp(timestamp: Union[datetime, int, float, None]) -> Optional[datetime]:
    """Formata um timestamp para datetime"""
    if timestamp is None:
        return None
    
    if isinstance(timestamp, (int, float)):
        # Converter timestamp Unix para datetime
        return datetime.fromtimestamp(timestamp)
    
    return timestamp

def calculate_risk_level(equipment_data: Dict[str, Any]) -> str:
    """Calcula o nível de risco de um equipamento com base em seus dados"""
    # Inicializar pontuação de risco
    risk_score = 0
    
    # Verificar idade do equipamento
    current_year = datetime.now().year
    equipment_year = equipment_data.get("year", current_year)
    age = current_year - equipment_year
    
    # Pontuação baseada na idade
    if age > 15:
        risk_score += 30
    elif age > 10:
        risk_score += 20
    elif age > 5:
        risk_score += 10
    
    # Verificar componentes
    components = equipment_data.get("components", [])
    for component in components:
        health = component.get("health_percentage", 100)
        if health < 30:
            risk_score += 30
        elif health < 50:
            risk_score += 20
        elif health < 70:
            risk_score += 10
    
    # Verificar dados operacionais
    operational_data = equipment_data.get("operational_data", [])
    if operational_data:
        # Ordenar por data
        operational_data.sort(key=lambda x: x.get("date", datetime.min))
        
        # Verificar últimos dados
        last_data = operational_data[-1]
        temperature = last_data.get("temperature")
        vibration = last_data.get("vibration")
        noise_level = last_data.get("noise_level")
        
        # Pontuação baseada em temperatura
        if temperature is not None:
            if temperature > 90:
                risk_score += 30
            elif temperature > 80:
                risk_score += 20
            elif temperature > 70:
                risk_score += 10
        
        # Pontuação baseada em vibração
        if vibration is not None:
            if vibration > 0.8:
                risk_score += 30
            elif vibration > 0.6:
                risk_score += 20
            elif vibration > 0.4:
                risk_score += 10
        
        # Pontuação baseada em nível de ruído
        if noise_level is not None:
            if noise_level > 90:
                risk_score += 30
            elif noise_level > 80:
                risk_score += 20
            elif noise_level > 70:
                risk_score += 10
    
    # Verificar horas de uso vs ciclo de manutenção
    usage_hours = equipment_data.get("usage_hours", 0)
    maintenance_cycle = equipment_data.get("maintenance_cycle", 1000)
    
    if maintenance_cycle > 0:
        usage_ratio = usage_hours / maintenance_cycle
        if usage_ratio > 1.5:
            risk_score += 30
        elif usage_ratio > 1.0:
            risk_score += 20
        elif usage_ratio > 0.8:
            risk_score += 10
    
    # Determinar nível de risco com base na pontuação
    if risk_score >= 50:
        return "high"
    elif risk_score >= 20:
        return "medium"
    else:
        return "low"

def validate_email(email: str) -> bool:
    """Valida um endereço de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Valida um número de telefone"""
    # Remover caracteres não numéricos
    digits = re.sub(r'\D', '', phone)
    # Verificar se tem entre 10 e 15 dígitos
    return 10 <= len(digits) <= 15

def format_currency(value: float) -> str:
    """Formata um valor para moeda (R$)"""
    return f"R$ {value:.2f}"

def calculate_mtbf(failures: List[Dict[str, Any]]) -> Optional[float]:
    """Calcula o Tempo Médio Entre Falhas (MTBF)"""
    if len(failures) < 2:
        return None
    
    # Ordenar falhas por data
    failures.sort(key=lambda x: x.get("date", datetime.min))
    
    # Calcular diferenças de tempo entre falhas consecutivas
    time_diffs = []
    for i in range(1, len(failures)):
        prev_date = failures[i-1].get("date")
        curr_date = failures[i].get("date")
        if prev_date and curr_date:
            diff_hours = (curr_date - prev_date).total_seconds() / 3600
            time_diffs.append(diff_hours)
    
    if not time_diffs:
        return None
    
    # Calcular média
    return sum(time_diffs) / len(time_diffs)

def calculate_reliability(mtbf: Optional[float], age_months: int) -> Optional[float]:
    """Calcula a confiabilidade com base no MTBF e idade"""
    if mtbf is None:
        return None
    
    # Fórmula simplificada de confiabilidade
    # R(t) = e^(-t/MTBF)
    t = age_months * 30 * 24  # Converter meses para horas
    reliability = math.exp(-t / mtbf) if mtbf > 0 else 0
    
    # Limitar entre 0 e 1
    return max(0, min(1, reliability))

def parse_date_range(from_date: Optional[datetime], to_date: Optional[datetime]) -> tuple:
    """Processa um intervalo de datas, definindo valores padrão se necessário"""
    if not to_date:
        to_date = datetime.utcnow()
    
    if not from_date:
        # Por padrão, 30 dias atrás
        from_date = to_date - timedelta(days=30)
    
    return from_date, to_date

def firestore_to_dict(doc_snapshot) -> Dict[str, Any]:
    """Converte um snapshot do Firestore para um dicionário"""
    data = doc_snapshot.to_dict()
    data["id"] = doc_snapshot.id
    return data

def handle_firebase_error(error: Exception) -> None:
    """Trata erros do Firebase e lança exceções HTTP apropriadas"""
    error_message = str(error)
    
    if "NOT_FOUND" in error_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso não encontrado"
        )
    elif "PERMISSION_DENIED" in error_message:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão negada para acessar este recurso"
        )
    elif "ALREADY_EXISTS" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Recurso já existe"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro do Firebase: {error_message}"
        )