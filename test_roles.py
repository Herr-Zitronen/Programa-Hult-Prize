from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal
from backend.app import models
import sys
import os

# Add backend to path if needed (might not be if running from root)
sys.path.append(os.path.join(os.getcwd(), 'backend'))

client = TestClient(app)

def test_create_role():
    print("Testing Role Creation API...")
    
    # 1. Clean DB (optional for test)
    db = SessionLocal()
    db.query(models.Role).delete()
    db.commit()
    db.close()

    # 2. Send POST request
    role_data = {
        "name": "Python Backend Developer",
        "description": "Expert in Python, FastAPI, and Database design."
    }
    
    response = client.post("/roles/", json=role_data)
    
    if response.status_code == 200:
        print("Success! Role created.")
        data = response.json()
        print(f"Role ID: {data['id']}")
        print(f"Role Name: {data['name']}")
        
        # 3. Verify embedding in DB
        db = SessionLocal()
        role = db.query(models.Role).filter(models.Role.id == data['id']).first()
        embedding = role.get_embedding()
        print(f"Embedding verified in DB. Length: {len(embedding)}")
        if len(embedding) > 0:
            print("Embedding generation SUCCESS.")
        else:
            print("Embedding generation FAILED.")
        db.close()
    else:
        print(f"Failed. Status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_create_role()
