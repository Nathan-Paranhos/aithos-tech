from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict, Any

from models.user import UserCreate, UserUpdate, User
from services import AuthService
from services.auth_service import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Dict[str, Any])
async def register(user_data: UserCreate = Body(...)):
    """Registra um novo usuário"""
    return await AuthService.register_user(user_data)

@router.post("/login", response_model=Dict[str, Any])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Autentica um usuário e retorna um token de acesso"""
    return await AuthService.login_user(form_data.username, form_data.password)

@router.post("/login/email", response_model=Dict[str, Any])
async def login_with_email(data: Dict[str, str] = Body(...)):
    """Autentica um usuário com email e senha e retorna um token de acesso"""
    if "email" not in data or "password" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email e senha são obrigatórios"
        )
    return await AuthService.login_user(data["email"], data["password"])

@router.post("/forgot-password", response_model=Dict[str, Any])
async def forgot_password(data: Dict[str, str] = Body(...)):
    """Envia um email para redefinição de senha"""
    if "email" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email é obrigatório"
        )
    return await AuthService.reset_password(data["email"])

@router.post("/reset-password", response_model=Dict[str, Any])
async def reset_password(data: Dict[str, str] = Body(...)):
    """Redefine a senha do usuário usando o código de verificação"""
    if "email" not in data or "code" not in data or "new_password" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email, código e nova senha são obrigatórios"
        )
    return await AuthService.confirm_reset_password(
        data["email"], data["code"], data["new_password"]
    )

@router.get("/me", response_model=User)
async def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=User)
async def update_current_user(
    user_data: UserUpdate = Body(...),
    current_user: User = Depends(get_current_user)
):
    """Atualiza informações do usuário atual"""
    return await AuthService.update_user(current_user.id, user_data)

@router.post("/logout", response_model=Dict[str, Any])
async def logout(current_user: User = Depends(get_current_user)):
    # Implement logout logic, e.g., invalidate token or log action
    return {"message": "Logout bem-sucedido"}