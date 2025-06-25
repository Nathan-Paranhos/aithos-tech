from typing import Dict, Any, List, Optional, Union, Tuple
import re
from datetime import datetime, timedelta
from fastapi import HTTPException, status

# Regex para validações comuns
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PHONE_REGEX = re.compile(r'^\+?[0-9]{10,15}$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$')

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """Valida se todos os campos obrigatórios estão presentes"""
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    
    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"
        )

def validate_email_format(email: str) -> bool:
    """Valida o formato de um endereço de email"""
    if not EMAIL_REGEX.match(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de email inválido"
        )
    return True

def validate_phone_format(phone: str) -> bool:
    """Valida o formato de um número de telefone"""
    if not PHONE_REGEX.match(phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de telefone inválido. Use o formato internacional (ex: +5511987654321)"
        )
    return True

def validate_password_strength(password: str) -> bool:
    """Valida a força da senha"""
    if not PASSWORD_REGEX.match(password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve ter pelo menos 8 caracteres, incluindo letras e números"
        )
    return True

def validate_date_format(date_str: str, format_str: str = "%Y-%m-%d") -> datetime:
    """Valida e converte uma string de data para objeto datetime"""
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato de data inválido. Use o formato {format_str}"
        )

def validate_date_range(start_date: Union[str, datetime], end_date: Union[str, datetime], 
                        format_str: str = "%Y-%m-%d") -> Tuple[datetime, datetime]:
    """Valida um intervalo de datas"""
    # Converter strings para datetime se necessário
    if isinstance(start_date, str):
        start_date = validate_date_format(start_date, format_str)
    
    if isinstance(end_date, str):
        end_date = validate_date_format(end_date, format_str)
    
    # Verificar se a data de início é anterior à data de fim
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A data de início deve ser anterior à data de fim"
        )
    
    return start_date, end_date

def validate_numeric_range(value: Union[int, float], min_value: Optional[Union[int, float]] = None, 
                          max_value: Optional[Union[int, float]] = None, field_name: str = "Valor") -> None:
    """Valida se um valor numérico está dentro de um intervalo específico"""
    if min_value is not None and value < min_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} deve ser maior ou igual a {min_value}"
        )
    
    if max_value is not None and value > max_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} deve ser menor ou igual a {max_value}"
        )

def validate_enum_value(value: Any, valid_values: List[Any], field_name: str = "Valor") -> None:
    """Valida se um valor está em uma lista de valores válidos"""
    if value not in valid_values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} deve ser um dos seguintes valores: {', '.join(map(str, valid_values))}"
        )

def validate_string_length(value: str, min_length: Optional[int] = None, 
                          max_length: Optional[int] = None, field_name: str = "Texto") -> None:
    """Valida o comprimento de uma string"""
    if min_length is not None and len(value) < min_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} deve ter pelo menos {min_length} caracteres"
        )
    
    if max_length is not None and len(value) > max_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} deve ter no máximo {max_length} caracteres"
        )

def validate_future_date(date_value: Union[str, datetime], format_str: str = "%Y-%m-%d", 
                        field_name: str = "Data") -> datetime:
    """Valida se uma data está no futuro"""
    # Converter string para datetime se necessário
    if isinstance(date_value, str):
        date_value = validate_date_format(date_value, format_str)
    
    # Verificar se a data é futura
    if date_value < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} deve ser uma data futura"
        )
    
    return date_value

def validate_list_not_empty(value_list: List[Any], field_name: str = "Lista") -> None:
    """Valida se uma lista não está vazia"""
    if not value_list or len(value_list) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} não pode estar vazia"
        )

def validate_unique_values(value_list: List[Any], field_name: str = "Lista") -> None:
    """Valida se todos os valores em uma lista são únicos"""
    if len(value_list) != len(set(value_list)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} contém valores duplicados"
        )