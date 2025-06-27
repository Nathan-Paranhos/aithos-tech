import pytest
from fastapi.testclient import TestClient
from main import app

# Cliente de teste do FastAPI
client = TestClient(app)

# -------------------------------
# Testes básicos de disponibilidade
# -------------------------------

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Bem-vindo" in data["message"]

# -------------------------------
# Testes de autenticação
# -------------------------------

def test_login_invalid_credentials():
    # Enviar como JSON (melhor compatibilidade com FastAPI)
    response = client.post(
        "/auth/login",
        json={"username": "usuario_inexistente", "password": "senha_incorreta"}
    )
    assert response.status_code == 401  # Unauthorized

def test_register_user(monkeypatch):
    # Mock da função register_user do AuthService
    async def mock_register_user(user_data):
        return {"message": "Usuário registrado com sucesso", "user_id": "mock-user-id"}
    
    from services import AuthService
    monkeypatch.setattr(AuthService, "register_user", mock_register_user)

    # Requisição com dados válidos de registro
    response = client.post(
        "/auth/register",
        json={
            "email": "teste@exemplo.com",
            "password": "Senha123",
            "name": "Usuário Teste",
            "phone": "+5511987654321"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "user_id" in data
    assert data["user_id"] == "mock-user-id"
