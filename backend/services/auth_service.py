from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from firebase_admin import auth as firebase_auth
from firebase_admin.exceptions import FirebaseError

from config import settings, db, pyrebase_auth
from models.user import UserCreate, User, UserInDB

# Configuração do contexto de criptografia para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para verificar senha
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar hash de senha
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Função para criar token de acesso JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Classe de serviço de autenticação
class AuthService:
    @staticmethod
    async def register_user(user_data: UserCreate) -> Dict[str, Any]:
        try:
            # Criar usuário no Firebase Authentication
            firebase_user = firebase_auth.create_user(
                email=user_data.email,
                password=user_data.password,
                display_name=user_data.display_name
            )
            
            # Criar documento do usuário no Firestore
            user_dict = {
                "email": user_data.email,
                "display_name": user_data.display_name,
                "company_name": user_data.company_name,
                "uid": firebase_user.uid,
                "role": "user",
                "created_at": datetime.utcnow(),
                "notification_preferences": {
                    "email": True,
                    "whatsapp": False,
                    "high_risk_only": False
                }
            }
            
            # Adicionar ao Firestore
            db.collection("users").document(firebase_user.uid).set(user_dict)
            
            # Gerar token de acesso
            access_token = create_access_token(
                data={"sub": firebase_user.uid, "email": user_data.email, "role": "user"}
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": firebase_user.uid,
                    "email": user_data.email,
                    "display_name": user_data.display_name,
                    "company_name": user_data.company_name,
                    "role": "user"
                }
            }
            
        except FirebaseError as e:
            if "EMAIL_EXISTS" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já está em uso"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao registrar usuário: {str(e)}"
            )
    
    @staticmethod
    async def login_user(email: str, password: str) -> Dict[str, Any]:
        try:
            # Autenticar com Firebase
            user = pyrebase_auth.sign_in_with_email_and_password(email, password)
            
            # Obter informações adicionais do usuário do Firestore
            user_doc = db.collection("users").document(user["localId"]).get()
            
            if not user_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuário não encontrado no banco de dados"
                )
            
            user_data = user_doc.to_dict()
            
            # Gerar token de acesso
            access_token = create_access_token(
                data={"sub": user["localId"], "email": email, "role": user_data.get("role", "user")}
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user["localId"],
                    "email": email,
                    "display_name": user_data.get("display_name", ""),
                    "company_name": user_data.get("company_name", ""),
                    "role": user_data.get("role", "user")
                }
            }
            
        except Exception as e:
            if "INVALID_PASSWORD" in str(e) or "INVALID_EMAIL" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Email ou senha incorretos"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao fazer login: {str(e)}"
            )
    
    @staticmethod
    async def reset_password(email: str) -> Dict[str, str]:
        try:
            # Enviar email de redefinição de senha
            firebase_auth.generate_password_reset_link(email)
            return {"message": "Email de redefinição de senha enviado com sucesso"}
        except FirebaseError as e:
            if "USER_NOT_FOUND" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Email não encontrado"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao enviar email de redefinição de senha: {str(e)}"
            )
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> User:
        try:
            user_doc = db.collection("users").document(user_id).get()
            
            if not user_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuário não encontrado"
                )
            
            user_data = user_doc.to_dict()
            user_data["id"] = user_id
            
            return User(**user_data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao buscar usuário: {str(e)}"
            )
    
    @staticmethod
    async def update_user(user_id: str, user_data: dict) -> User:
        try:
            # Atualizar no Firestore
            user_data["updated_at"] = datetime.utcnow()
            db.collection("users").document(user_id).update(user_data)
            
            # Buscar usuário atualizado
            updated_user = await AuthService.get_user_by_id(user_id)
            return updated_user
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao atualizar usuário: {str(e)}"
            )