import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.ai_engine import AIEngine
from app.database import engine, Base
from app import models

def test_setup():
    print("Testing AI Engine...")
    ai = AIEngine()
    embedding = ai.get_embedding("This is a test")
    print(f"Embedding generated. Shape: {len(embedding)}")

    print("Testing Database...")
    models.Base.metadata.create_all(bind=engine)
    if os.path.exists("./backend/data/recruit.db"):
        print("Database created successfully.")
    else:
        print("Database file NOT found.")

if __name__ == "__main__":
    test_setup()
