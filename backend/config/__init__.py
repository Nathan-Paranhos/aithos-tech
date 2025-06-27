# Importações reorganizadas para evitar dependências circulares
# Importando apenas de settings.py, não de app.py para evitar conflitos
from .settings import settings
from .firebase import db, firebase_auth, bucket, pyrebase_auth, pyrebase_storage, pyrebase_db, firebase_config
from .database import firestore_manager