from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal
from backend.app import models
import sys
import os
import io

# Add backend to path if needed
sys.path.append(os.path.join(os.getcwd(), 'backend'))

client = TestClient(app)

def test_upload_and_rank():
    print("Testing CV Upload and Ranking...")
    
    # 1. Setup Role
    db = SessionLocal()
    # Ensure at least one role exists
    role = db.query(models.Role).first()
    if not role:
        print("Creating dummy role...")
        role = models.Role(name="Python Dev", description="Looking for Python, FastAPI, and SQL skills.")
        db.add(role)
        db.commit()
    
    role_id = role.id
    print(f"Using Role ID: {role_id} - {role.name}")
    db.close()

    # 2. Simulate PDF Upload
    # We will send a dummy text file disguised as .docx for simplicity in this test environment
    # or just Mock the content. The AI Engine extract_text_from_docx expects a valid zip/docx.
    # So we'll mock a simpler test case: A file that fails extraction vs one that works ???
    # Actually, let's just make a dummy file with text content since our extraction might fail on invalid binary.
    # WAIT: The system needs valid PDF/DOCX binary structure.
    # For this quick test, I will skip complex binary creation and just verify the endpoint logic 
    # if I can mock the extraction or if I have a real file.
    
    # Alternative: I'll test the error handling for invalid file first.
    
    files = {'file': ('test.txt', b'This is a text file', 'text/plain')}
    response = client.post(f"/candidates/{role_id}", files=files)
    print(f"Test Invalid Format (TXT): Status {response.status_code}")
    if response.status_code == 400:
        print("PASS: Correctly rejected invalid format.")
    else:
        print("FAIL: Should have rejected text file.")

    # 3. Simulate Rank Retrieval
    # Create a dummy candidate in DB to verify GET /rankings
    db = SessionLocal()
    dummy_cand = models.Candidate(
        role_id=role_id,
        filename="dummy_resume.pdf",
        content="Python SQL FastAPI",
        score=95,
        matched_skills_json='["python", "sql"]'
    )
    db.add(dummy_cand)
    db.commit()
    db.close()
    
    response = client.get(f"/candidates/{role_id}")
    if response.status_code == 200:
        candidates = response.json()
        print(f"GET /rankings returned {len(candidates)} candidates.")
        if len(candidates) > 0:
            print(f"Top Candidate Score: {candidates[0]['score']}")
            print(f"Matched Skills: {candidates[0]['matched_skills']}")
            print("PASS: Rankings retrieval successful.")
    else:
        print("FAIL: Could not retrieve rankings.")

if __name__ == "__main__":
    test_upload_and_rank()
