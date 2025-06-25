import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
import pyrebase
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do Firebase Admin SDK
firebase_config = {
    "apiKey": "AIzaSyC9d3V4KWpGiSl5vzKZ16ycwoZqldLo2zI",
    "authDomain": "hackaton-anchieta.firebaseapp.com",
    "projectId": "hackaton-anchieta",
    "storageBucket": "hackaton-anchieta.firebasestorage.app",
    "messagingSenderId": "585293268662",
    "appId": "1:585293268662:web:5a15c69ba1347b2d404817",
    "measurementId": "G-MEPT9NZS7B",
    "databaseURL": "https://hackaton-anchieta.firebaseio.com"
}

# Caminho para o arquivo de credenciais do Firebase Admin SDK
# Normalmente, você baixaria este arquivo do console do Firebase
# e o colocaria em um local seguro no seu servidor
cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "./serviceAccountKey.json")

# Inicializa o Firebase Admin SDK se o arquivo de credenciais existir
try:
    # Verifica se já foi inicializado
    if not firebase_admin._apps:
        # Se o arquivo de credenciais existir, use-o
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                'storageBucket': firebase_config['storageBucket']
            })
        # Caso contrário, inicialize com as credenciais do ambiente
        else:
            firebase_admin.initialize_app()
    
    # Obtém instâncias dos serviços
    db = firestore.client()
    firebase_auth = auth
    bucket = storage.bucket()
    
    print("Firebase Admin SDK inicializado com sucesso.")
except Exception as e:
    print(f"Erro ao inicializar Firebase Admin SDK: {e}")
    db = None
    firebase_auth = None
    bucket = None

# Inicializa o Pyrebase para operações do lado do cliente
pyrebase_app = pyrebase.initialize_app(firebase_config)
pyrebase_auth = pyrebase_app.auth()
pyrebase_storage = pyrebase_app.storage()
pyrebase_db = pyrebase_app.database()

# Exporta as instâncias para uso em outros módulos
__all__ = ['db', 'firebase_auth', 'bucket', 'pyrebase_auth', 'pyrebase_storage', 'pyrebase_db', 'firebase_config']