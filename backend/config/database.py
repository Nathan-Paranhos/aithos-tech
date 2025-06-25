from typing import Dict, Any, List, Optional
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime

from .firebase import db
from utils.helpers import firestore_to_dict

class FirestoreManager:
    """Classe para gerenciar operações no Firestore"""
    
    @staticmethod
    async def get_document(collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Obtém um documento pelo ID"""
        try:
            doc_ref = db.collection(collection).document(doc_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return firestore_to_dict(doc)
            return None
        except Exception as e:
            print(f"Erro ao obter documento: {str(e)}")
            return None
    
    @staticmethod
    async def get_documents(collection: str, filters: Optional[List[Dict[str, Any]]] = None, 
                           order_by: Optional[str] = None, limit: Optional[int] = None, 
                           start_after: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Obtém múltiplos documentos com filtros opcionais"""
        try:
            query = db.collection(collection)
            
            # Aplicar filtros
            if filters:
                for filter_item in filters:
                    field = filter_item.get('field')
                    op = filter_item.get('op', '==')
                    value = filter_item.get('value')
                    
                    if field and value is not None:
                        query = query.where(filter=FieldFilter(field, op, value))
            
            # Aplicar ordenação
            if order_by:
                direction = firestore.Query.DESCENDING if order_by.startswith('-') else firestore.Query.ASCENDING
                field = order_by[1:] if order_by.startswith('-') else order_by
                query = query.order_by(field, direction=direction)
            
            # Aplicar paginação
            if start_after:
                query = query.start_after(start_after)
            
            # Aplicar limite
            if limit:
                query = query.limit(limit)
            
            # Executar consulta
            docs = query.stream()
            return [firestore_to_dict(doc) for doc in docs]
        except Exception as e:
            print(f"Erro ao obter documentos: {str(e)}")
            return []
    
    @staticmethod
    async def create_document(collection: str, data: Dict[str, Any], doc_id: Optional[str] = None) -> Optional[str]:
        """Cria um novo documento"""
        try:
            # Adicionar timestamp de criação
            data['created_at'] = datetime.now()
            data['updated_at'] = datetime.now()
            
            if doc_id:
                # Usar ID fornecido
                doc_ref = db.collection(collection).document(doc_id)
                doc_ref.set(data)
                return doc_id
            else:
                # Gerar ID automático
                doc_ref = db.collection(collection).add(data)
                return doc_ref[1].id
        except Exception as e:
            print(f"Erro ao criar documento: {str(e)}")
            return None
    
    @staticmethod
    async def update_document(collection: str, doc_id: str, data: Dict[str, Any]) -> bool:
        """Atualiza um documento existente"""
        try:
            # Adicionar timestamp de atualização
            data['updated_at'] = datetime.now()
            
            doc_ref = db.collection(collection).document(doc_id)
            doc_ref.update(data)
            return True
        except Exception as e:
            print(f"Erro ao atualizar documento: {str(e)}")
            return False
    
    @staticmethod
    async def delete_document(collection: str, doc_id: str) -> bool:
        """Exclui um documento"""
        try:
            doc_ref = db.collection(collection).document(doc_id)
            doc_ref.delete()
            return True
        except Exception as e:
            print(f"Erro ao excluir documento: {str(e)}")
            return False
    
    @staticmethod
    async def count_documents(collection: str, filters: Optional[List[Dict[str, Any]]] = None) -> int:
        """Conta o número de documentos em uma coleção"""
        try:
            query = db.collection(collection)
            
            # Aplicar filtros
            if filters:
                for filter_item in filters:
                    field = filter_item.get('field')
                    op = filter_item.get('op', '==')
                    value = filter_item.get('value')
                    
                    if field and value is not None:
                        query = query.where(filter=FieldFilter(field, op, value))
            
            # Executar consulta e contar documentos
            docs = query.stream()
            return sum(1 for _ in docs)
        except Exception as e:
            print(f"Erro ao contar documentos: {str(e)}")
            return 0
    
    @staticmethod
    async def batch_create(collection: str, items: List[Dict[str, Any]]) -> List[str]:
        """Cria múltiplos documentos em lote"""
        try:
            batch = db.batch()
            doc_refs = []
            
            for item in items:
                # Adicionar timestamps
                item['created_at'] = datetime.now()
                item['updated_at'] = datetime.now()
                
                # Criar referência e adicionar ao lote
                doc_ref = db.collection(collection).document()
                batch.set(doc_ref, item)
                doc_refs.append(doc_ref)
            
            # Executar operação em lote
            batch.commit()
            
            # Retornar IDs dos documentos criados
            return [doc_ref.id for doc_ref in doc_refs]
        except Exception as e:
            print(f"Erro ao criar documentos em lote: {str(e)}")
            return []
    
    @staticmethod
    async def batch_update(collection: str, items: List[Dict[str, Any]]) -> bool:
        """Atualiza múltiplos documentos em lote"""
        try:
            batch = db.batch()
            
            for item in items:
                doc_id = item.get('id')
                if not doc_id:
                    continue
                
                # Remover ID do objeto de dados
                data = {k: v for k, v in item.items() if k != 'id'}
                
                # Adicionar timestamp de atualização
                data['updated_at'] = datetime.now()
                
                # Adicionar ao lote
                doc_ref = db.collection(collection).document(doc_id)
                batch.update(doc_ref, data)
            
            # Executar operação em lote
            batch.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar documentos em lote: {str(e)}")
            return False
    
    @staticmethod
    async def batch_delete(collection: str, doc_ids: List[str]) -> bool:
        """Exclui múltiplos documentos em lote"""
        try:
            batch = db.batch()
            
            for doc_id in doc_ids:
                doc_ref = db.collection(collection).document(doc_id)
                batch.delete(doc_ref)
            
            # Executar operação em lote
            batch.commit()
            return True
        except Exception as e:
            print(f"Erro ao excluir documentos em lote: {str(e)}")
            return False

# Exportar instância para uso em outros módulos
firestore_manager = FirestoreManager()