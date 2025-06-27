import pytest
import uuid
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from models.equipment import Equipment, OperationalData
from services.equipment_service import EquipmentService

# Dados de teste
@pytest.fixture
def sample_equipment_data():
    return {
        "name": "Trator Teste",
        "model": "Modelo X-123",
        "manufacturer": "Fabricante Teste",
        "year": 2020,
        "category": "agricultural",
        "serial_number": "SN12345678",
        "purchase_date": datetime.now().strftime("%Y-%m-%d"),
        "location": "Fazenda Teste",
        "status": "active",
        "description": "Equipamento para testes"
    }

@pytest.fixture
def sample_operational_data():
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "hours_operated": 120,
        "temperature": 75.5,
        "vibration": 0.8,
        "pressure": 45.2,
        "oil_level": 0.85,
        "fuel_consumption": 12.3,
        "notes": "Dados operacionais de teste"
    }

# Testes para o serviço de equipamentos
class TestEquipmentService:
    
    @patch('services.equipment_service.db')
    async def test_create_equipment(self, mock_db, sample_equipment_data):
        # Configurar o mock
        mock_doc = MagicMock()
        mock_doc.id = "test-equipment-id"
        mock_db.collection.return_value.document.return_value = mock_doc
        
        # Chamar o método a ser testado
        user_id = "test-user-id"
        result = await EquipmentService.create_equipment(sample_equipment_data, user_id)
        
        # Verificar o resultado
        assert result["id"] == "test-equipment-id"
        assert "message" in result
        
        # Verificar se o método set foi chamado com os dados corretos
        mock_db.collection.assert_called_once_with("equipments")
        mock_db.collection.return_value.document.assert_called_once()
        mock_doc.set.assert_called_once()
        
        # Verificar se os dados passados para o set incluem o user_id
        set_data = mock_doc.set.call_args[0][0]
        assert set_data["user_id"] == user_id
        assert set_data["name"] == sample_equipment_data["name"]
    
    @patch('services.equipment_service.db')
    async def test_get_equipment_by_id(self, mock_db):
        # Configurar o mock
        mock_doc = MagicMock()
        mock_doc.to_dict.return_value = {
            "id": "test-equipment-id",
            "name": "Trator Teste",
            "user_id": "test-user-id",
            "operational_data": []
        }
        mock_doc.id = "test-equipment-id"
        mock_db.collection.return_value.document.return_value.get.return_value = mock_doc
        
        # Chamar o método a ser testado
        equipment_id = "test-equipment-id"
        user_id = "test-user-id"
        result = await EquipmentService.get_equipment_by_id(equipment_id, user_id)
        
        # Verificar o resultado
        assert isinstance(result, Equipment)
        assert result.id == "test-equipment-id"
        assert result.name == "Trator Teste"
        
        # Verificar se os métodos do mock foram chamados corretamente
        mock_db.collection.assert_called_once_with("equipments")
        mock_db.collection.return_value.document.assert_called_once_with(equipment_id)
        mock_db.collection.return_value.document.return_value.get.assert_called_once()
    
    @patch('services.equipment_service.db')
    async def test_add_operational_data(self, mock_db, sample_operational_data):
        # Configurar o mock para get_equipment_by_id
        equipment = Equipment(
            id="test-equipment-id",
            name="Trator Teste",
            model="Modelo X-123",
            manufacturer="Fabricante Teste",
            year=2020,
            category="agricultural",
            user_id="test-user-id",
            operational_data=[]
        )
        
        # Patch para o método get_equipment_by_id
        with patch.object(EquipmentService, 'get_equipment_by_id', return_value=equipment) as mock_get:
            # Configurar o mock para document.update
            mock_update = MagicMock()
            mock_db.collection.return_value.document.return_value.update = mock_update
            
            # Chamar o método a ser testado
            equipment_id = "test-equipment-id"
            user_id = "test-user-id"
            result = await EquipmentService.add_operational_data(equipment_id, sample_operational_data, user_id)
            
            # Verificar o resultado
            assert "message" in result
            assert result["data_id"] is not None
            
            # Verificar se os métodos do mock foram chamados corretamente
            mock_get.assert_called_once_with(equipment_id, user_id)
            mock_db.collection.assert_called_once_with("equipments")
            mock_db.collection.return_value.document.assert_called_once_with(equipment_id)
            mock_update.assert_called_once()
            
            # Verificar se os dados operacionais foram adicionados corretamente
            update_data = mock_update.call_args[0][0]
            assert "operational_data" in update_data
            assert len(update_data["operational_data"]) == 1