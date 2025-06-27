import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Fixture que fornece um cliente de teste para a API FastAPI."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def mock_firebase_db():
    """Fixture para simular o banco de dados Firebase.
    
    Esta fixture pode ser expandida para simular diferentes comportamentos
    do banco de dados durante os testes.
    """
    class MockFirestore:
        def collection(self, name):
            return MockCollection(name)
    
    class MockCollection:
        def __init__(self, name):
            self.name = name
            self.documents = {}
        
        def document(self, doc_id):
            if doc_id not in self.documents:
                self.documents[doc_id] = MockDocument(doc_id)
            return self.documents[doc_id]
        
        def where(self, field, op, value):
            # Simula a funcionalidade de filtro
            return self
        
        def get(self):
            # Retorna uma lista de documentos simulados
            return [doc for doc in self.documents.values()]
    
    class MockDocument:
        def __init__(self, doc_id):
            self.id = doc_id
            self.data = {}
        
        def set(self, data, merge=False):
            if merge:
                self.data.update(data)
            else:
                self.data = data
            return self
        
        def get(self):
            return self
        
        def to_dict(self):
            return self.data
        
        def update(self, data):
            self.data.update(data)
            return self
        
        def delete(self):
            # Simula a exclusão do documento
            pass
    
    return MockFirestore()