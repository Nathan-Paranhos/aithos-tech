import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import jwt

from fastapi import HTTPException
from models.user import User, UserCreate
from services.auth_service import AuthService, get_current_user
from config.settings import settings

# Fixtures para testes
@pytest.fixture
def sample_user_data():
    return UserCreate(
        email="teste@exemplo.com",
        password="Senha123",
        name="Usuário Teste",
        phone="+5511987654321"
    )

@pytest.fixture
def sample_user():
    return User(
        id="test-user-id",
        email="teste@exemplo.com",
        name="Usuário Teste",
        phone="+5511987654321",
        role="user",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@pytest.fixture
def sample_token():
    # Criar um token JWT válido para testes
    payload = {
        "sub": "test-user-id",
        "email": "teste@exemplo.com",
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

# Testes para o serviço de autenticação
class TestAuthService:
    
    @patch('services.auth_service.pyrebase_auth')
    @patch('services.auth_service.db')
    async def test_register_user(self, mock_db, mock_pyrebase_auth, sample_user_data):
        # Configurar mocks
        mock_pyrebase_auth.create_user_with_email_and_password.return_value = {
            "localId": "test-user-id",
            "email": sample_user_data.email
        }
        
        mock_doc = MagicMock()
        mock_doc.id = "test-user-id"
        mock_db.collection.return_value.document.return_value = mock_doc
        
        # Chamar o método a ser testado
        result = await AuthService.register_user(sample_user_data)
        
        # Verificar o resultado
        assert result["user_id"] == "test-user-id"
        assert "message" in result
        
        # Verificar se os métodos do mock foram chamados corretamente
        mock_pyrebase_auth.create_user_with_email_and_password.assert_called_once_with(
            sample_user_data.email, sample_user_data.password
        )
        mock_db.collection.assert_called_once_with("users")
        mock_db.collection.return_value.document.assert_called_once_with("test-user-id")
        mock_doc.set.assert_called_once()
        
        # Verificar se os dados do usuário foram armazenados corretamente
        set_data = mock_doc.set.call_args[0][0]
        assert set_data["email"] == sample_user_data.email
        assert set_data["name"] == sample_user_data.name
        assert "password" not in set_data  # Senha não deve ser armazenada
    
    @patch('services.auth_service.pyrebase_auth')
    @patch('services.auth_service.create_access_token')
    async def test_login_user(self, mock_create_token, mock_pyrebase_auth):
        # Configurar mocks
        mock_pyrebase_auth.sign_in_with_email_and_password.return_value = {
            "localId": "test-user-id",
            "email": "teste@exemplo.com",
            "idToken": "firebase-token"
        }
        
        mock_create_token.return_value = "jwt-token"
        
        # Chamar o método a ser testado
        email = "teste@exemplo.com"
        password = "Senha123"
        result = await AuthService.login_user(email, password)
        
        # Verificar o resultado
        assert result["access_token"] == "jwt-token"
        assert result["token_type"] == "bearer"
        
        # Verificar se os métodos do mock foram chamados corretamente
        mock_pyrebase_auth.sign_in_with_email_and_password.assert_called_once_with(email, password)
        mock_create_token.assert_called_once_with({"sub": "test-user-id", "email": email})
    
    @patch('services.auth_service.pyrebase_auth')
    async def test_login_user_invalid_credentials(self, mock_pyrebase_auth):
        # Configurar mock para simular credenciais inválidas
        mock_pyrebase_auth.sign_in_with_email_and_password.side_effect = Exception("Invalid credentials")
        
        # Chamar o método a ser testado e verificar se lança exceção
        with pytest.raises(HTTPException) as exc_info:
            await AuthService.login_user("teste@exemplo.com", "senha_incorreta")
        
        # Verificar a exceção
        assert exc_info.value.status_code == 401
        assert "Credenciais inválidas" in str(exc_info.value.detail)
    
    @patch('services.auth_service.jwt')
    @patch('services.auth_service.db')
    async def test_get_current_user(self, mock_db, mock_jwt, sample_user, sample_token):
        # Configurar mocks
        mock_jwt.decode.return_value = {"sub": "test-user-id", "email": "teste@exemplo.com"}
        
        mock_doc = MagicMock()
        mock_doc.to_dict.return_value = sample_user.dict()
        mock_doc.id = "test-user-id"
        mock_db.collection.return_value.document.return_value.get.return_value = mock_doc
        
        # Chamar o método a ser testado
        user = await get_current_user(sample_token)
        
        # Verificar o resultado
        assert user.id == "test-user-id"
        assert user.email == "teste@exemplo.com"
        
        # Verificar se os métodos do mock foram chamados corretamente
        mock_jwt.decode.assert_called_once_with(
            sample_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        mock_db.collection.assert_called_once_with("users")
        mock_db.collection.return_value.document.assert_called_once_with("test-user-id")
        mock_db.collection.return_value.document.return_value.get.assert_called_once()
    
    @patch('services.auth_service.jwt')
    async def test_get_current_user_invalid_token(self, mock_jwt):
        # Configurar mock para simular token inválido
        mock_jwt.decode.side_effect = jwt.PyJWTError("Invalid token")
        
        # Chamar o método a ser testado e verificar se lança exceção
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user("token-invalido")
        
        # Verificar a exceção
        assert exc_info.value.status_code == 401
        assert "Token inválido" in str(exc_info.value.detail)