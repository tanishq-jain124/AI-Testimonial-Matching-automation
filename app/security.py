from passlib.context import CryptContext
from itsdangerous import URLSafeSerializer
from app.config import settings

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
serializer = URLSafeSerializer(settings.APP_SECRET, salt="yearbook-session")

def hash_password(password: str) -> str:
    return pwd.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd.verify(password, password_hash)

def make_session(user_id: int) -> str:
    return serializer.dumps({"user_id": user_id})

def read_session(token: str):
    try:
        return int(serializer.loads(token)["user_id"])
    except Exception:
        return None
