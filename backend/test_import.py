from config.app import Settings

print("Importação bem-sucedida!")
print("Configurações carregadas:")
settings = Settings()
print(f"APP_NAME: {settings.APP_NAME}")
print(f"DEBUG: {settings.DEBUG}")