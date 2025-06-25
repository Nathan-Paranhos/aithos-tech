from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
import firebase_admin.auth
from firebase_admin.exceptions import FirebaseError

from config import settings

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Verifica o token JWT do Firebase e retorna os dados do usuário"""
    token = credentials.credentials
    try:
        # Verificar token com Firebase Admin SDK
        decoded_token = firebase_admin.auth.verify_id_token(token)
        return decoded_token
    except FirebaseError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Erro na autenticação: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )

async def get_current_user_id(token_data: Dict[str, Any] = Depends(verify_token)) -> str:
    """Extrai o ID do usuário do token verificado"""
    if "uid" not in token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não contém ID de usuário",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return token_data["uid"]

async def get_current_user_role(token_data: Dict[str, Any] = Depends(verify_token)) -> str:
    """Extrai o papel (role) do usuário do token verificado"""
    # O papel pode estar em claims personalizadas
    if "claims" in token_data and "role" in token_data["claims"]:
        return token_data["claims"]["role"]
    # Ou pode estar diretamente no token
    if "role" in token_data:
        return token_data["role"]
    # Papel padrão se não for encontrado
    return "user"

async def require_admin(role: str = Depends(get_current_user_role)):
    """Verifica se o usuário tem papel de administrador"""
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )
    return True

class RateLimiter:
    """Implementação simples de limitação de taxa"""
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = {}
        self.cleanup_interval = 60  # Limpar registros a cada 60 segundos
    
    async def check(self, request: Request):
        """Verifica se o cliente excedeu o limite de requisições"""
        # Implementação simplificada - em produção, use Redis ou similar
        client_ip = request.client.host
        current_time = int(request.scope.get("time", 0))
        
        # Limpar registros antigos
        if client_ip in self.requests:
            self.requests[client_ip] = [t for t in self.requests[client_ip] if current_time - t < self.cleanup_interval]
        else:
            self.requests[client_ip] = []
        
        # Verificar limite
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Limite de requisições excedido. Tente novamente mais tarde."
            )
        
        # Registrar requisição
        self.requests[client_ip].append(current_time)
        
        return True

# Instância global do limitador de taxa
rate_limiter = RateLimiter()

async def rate_limit(request: Request):
    """Middleware para limitar a taxa de requisições"""
    return await rate_limiter.check(request)