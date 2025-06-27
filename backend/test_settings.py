# Script para testar a importação da classe Settings

try:
    # Importar diretamente do módulo settings.py
    from config.settings import settings
    print("Importação bem-sucedida!")
    
    # Usar a instância já criada
    print(f"APP_NAME: {settings.APP_NAME}")
    print(f"DEBUG: {settings.DEBUG}")
    print("Teste concluído com sucesso!")
    
except Exception as e:
    print(f"Erro ao importar settings: {e}")
    import traceback
    traceback.print_exc()