import uvicorn
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter configurações do servidor do arquivo .env ou usar valores padrão
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "8000"))
debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

if __name__ == "__main__":
    print(f"Iniciando servidor AgroGuard em {host}:{port}")
    print(f"Modo de depuração: {'Ativado' if debug else 'Desativado'}")
    
    # Iniciar o servidor Uvicorn
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="debug" if debug else "info"
    )