# Testes da API AgroGuard

Este diretório contém os testes automatizados para a API AgroGuard. Os testes são escritos usando o framework pytest e o cliente de teste do FastAPI.

## Estrutura de Testes

- `conftest.py`: Contém fixtures reutilizáveis para os testes
- `test_api.py`: Testes de integração para os endpoints da API
- `test_equipment_service.py`: Testes unitários para o serviço de equipamentos

## Como Executar os Testes

Para executar todos os testes, navegue até o diretório raiz do backend e execute:

```bash
pytest
```

Para executar testes específicos:

```bash
pytest tests/test_api.py
pytest tests/test_equipment_service.py
```

Para executar testes com relatório de cobertura:

```bash
pytest --cov=. tests/
```

Para gerar um relatório HTML de cobertura:

```bash
pytest --cov=. --cov-report=html tests/
```

## Melhores Práticas

1. **Isolamento**: Cada teste deve ser independente e não depender do estado de outros testes.

2. **Mocking**: Use mocks para simular dependências externas como o Firebase.

3. **Fixtures**: Use fixtures do pytest para reutilizar código de configuração.

4. **Nomenclatura**: Nomeie os testes de forma descritiva, começando com `test_`.

5. **Organização**: Organize os testes em classes para agrupar testes relacionados.

6. **Cobertura**: Tente manter uma boa cobertura de testes, especialmente para lógica de negócios crítica.

## Testando Endpoints Protegidos

Para testar endpoints que requerem autenticação, você pode usar a fixture `client` e simular a autenticação:

```python
def test_protected_endpoint(client):
    # Simular um token JWT válido
    headers = {"Authorization": f"Bearer {fake_token}"}
    response = client.get("/endpoint-protegido", headers=headers)
    assert response.status_code == 200
```

Alternativamente, você pode fazer patch na função `get_current_user` para retornar um usuário de teste:

```python
from unittest.mock import patch
from models.user import User

def test_protected_endpoint_with_mock(client):
    # Criar um usuário de teste
    test_user = User(id="test-id", email="test@example.com", name="Test User")
    
    # Fazer patch na função get_current_user
    with patch("services.auth_service.get_current_user", return_value=test_user):
        response = client.get("/endpoint-protegido")
        assert response.status_code == 200
```

## Testando Serviços com Firebase

Para testar serviços que dependem do Firebase, use a fixture `mock_firebase_db` definida em `conftest.py`:

```python
def test_service_with_firebase(mock_firebase_db):
    # Configurar o mock
    with patch("services.some_service.db", mock_firebase_db):
        # Executar o teste
        result = some_service_function()
        assert result == expected_result
```