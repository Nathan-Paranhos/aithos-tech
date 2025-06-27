from typing import Dict, Any, Optional, BinaryIO, Union
import os
import uuid
from datetime import datetime
from fastapi import UploadFile, HTTPException, status
from firebase_admin import storage
import tempfile

from config.firebase import bucket

class StorageManager:
    """Classe para gerenciar operações de armazenamento de arquivos"""
    
    @staticmethod
    async def upload_file(file: UploadFile, folder: str = "uploads") -> Dict[str, Any]:
        """Faz upload de um arquivo para o Firebase Storage"""
        try:
            # Gerar nome único para o arquivo
            file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = f"{folder}/{unique_filename}"
            
            # Criar arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                # Ler conteúdo do arquivo enviado
                content = await file.read()
                # Escrever no arquivo temporário
                temp_file.write(content)
                temp_file.flush()
            
            # Fazer upload para o Firebase Storage
            blob = bucket.blob(file_path)
            blob.upload_from_filename(temp_file.name)
            
            # Definir metadados
            blob.metadata = {
                "contentType": file.content_type,
                "originalName": file.filename,
                "uploadedAt": datetime.now().isoformat()
            }
            blob.patch()
            
            # Gerar URL pública
            blob.make_public()
            public_url = blob.public_url
            
            # Remover arquivo temporário
            os.unlink(temp_file.name)
            
            return {
                "filename": unique_filename,
                "original_filename": file.filename,
                "content_type": file.content_type,
                "size": len(content),
                "path": file_path,
                "url": public_url,
                "uploaded_at": datetime.now().isoformat()
            }
        except Exception as e:
            # Garantir que o arquivo temporário seja removido em caso de erro
            if 'temp_file' in locals() and os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
            
            print(f"Erro ao fazer upload do arquivo: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao fazer upload do arquivo: {str(e)}"
            )
    
    @staticmethod
    async def upload_file_from_bytes(file_bytes: bytes, filename: str, content_type: str, folder: str = "uploads") -> Dict[str, Any]:
        """Faz upload de bytes para o Firebase Storage"""
        try:
            # Gerar nome único para o arquivo
            file_extension = os.path.splitext(filename)[1] if filename else ""
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = f"{folder}/{unique_filename}"
            
            # Criar arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                # Escrever bytes no arquivo temporário
                temp_file.write(file_bytes)
                temp_file.flush()
            
            # Fazer upload para o Firebase Storage
            blob = bucket.blob(file_path)
            blob.upload_from_filename(temp_file.name)
            
            # Definir metadados
            blob.metadata = {
                "contentType": content_type,
                "originalName": filename,
                "uploadedAt": datetime.now().isoformat()
            }
            blob.patch()
            
            # Gerar URL pública
            blob.make_public()
            public_url = blob.public_url
            
            # Remover arquivo temporário
            os.unlink(temp_file.name)
            
            return {
                "filename": unique_filename,
                "original_filename": filename,
                "content_type": content_type,
                "size": len(file_bytes),
                "path": file_path,
                "url": public_url,
                "uploaded_at": datetime.now().isoformat()
            }
        except Exception as e:
            # Garantir que o arquivo temporário seja removido em caso de erro
            if 'temp_file' in locals() and os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
            
            print(f"Erro ao fazer upload do arquivo: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao fazer upload do arquivo: {str(e)}"
            )
    
    @staticmethod
    async def download_file(file_path: str) -> Optional[bytes]:
        """Baixa um arquivo do Firebase Storage"""
        try:
            # Obter blob
            blob = bucket.blob(file_path)
            
            # Verificar se o arquivo existe
            if not blob.exists():
                return None
            
            # Baixar para memória
            return blob.download_as_bytes()
        except Exception as e:
            print(f"Erro ao baixar arquivo: {str(e)}")
            return None
    
    @staticmethod
    async def delete_file(file_path: str) -> bool:
        """Exclui um arquivo do Firebase Storage"""
        try:
            # Obter blob
            blob = bucket.blob(file_path)
            
            # Verificar se o arquivo existe
            if not blob.exists():
                return False
            
            # Excluir arquivo
            blob.delete()
            return True
        except Exception as e:
            print(f"Erro ao excluir arquivo: {str(e)}")
            return False
    
    @staticmethod
    async def get_file_metadata(file_path: str) -> Optional[Dict[str, Any]]:
        """Obtém metadados de um arquivo no Firebase Storage"""
        try:
            # Obter blob
            blob = bucket.blob(file_path)
            
            # Verificar se o arquivo existe
            if not blob.exists():
                return None
            
            # Obter metadados
            blob.reload()
            
            return {
                "name": blob.name,
                "bucket": blob.bucket.name,
                "content_type": blob.content_type,
                "size": blob.size,
                "updated": blob.updated,
                "metadata": blob.metadata,
                "public_url": blob.public_url if blob.public else None
            }
        except Exception as e:
            print(f"Erro ao obter metadados do arquivo: {str(e)}")
            return None

# Exportar instância para uso em outros módulos
storage_manager = StorageManager()