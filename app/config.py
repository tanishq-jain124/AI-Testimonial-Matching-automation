import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_SECRET = os.getenv("APP_SECRET", "dev-secret-change-me")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./yearbook.db")
    
    # ✅ Updated Groq with new model
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")  # 👈 Updated
    
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.80"))
    MAX_GENERATION_ATTEMPTS = int(os.getenv("MAX_GENERATION_ATTEMPTS", "3"))
    MAX_CHAT_CONTEXT = int(os.getenv("MAX_CHAT_CONTEXT", "30"))
    MAX_SOCIAL_TEXT = int(os.getenv("MAX_SOCIAL_TEXT", "8000"))

settings = Settings()