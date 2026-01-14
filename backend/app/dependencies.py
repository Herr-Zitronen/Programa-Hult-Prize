from .database import SessionLocal
from .services.ai_engine import AIEngine

# Global instance for AI Engine (Singleton pattern)
_ai_engine_instance = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_ai_engine():
    global _ai_engine_instance
    if _ai_engine_instance is None:
        _ai_engine_instance = AIEngine()
    return _ai_engine_instance
