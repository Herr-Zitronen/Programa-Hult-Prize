from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

# Internal imports
from .. import models, schemas, dependencies
from ..services.ai_engine import AIEngine

router = APIRouter(
    prefix="/candidates",
    tags=["candidates"],
    responses={404: {"description": "Not found"}},
)

@router.post("/{role_id}", response_model=schemas.CandidateResponse)
async def process_cv(
    role_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(dependencies.get_db),
    ai: AIEngine = Depends(dependencies.get_ai_engine)
):
    # 1. Check if Role exists
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # 2. Read File
    try:
        content = await file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Error reading file")

    # 3. Extract Text (Safety first)
    text = ""
    try:
        if file.filename.lower().endswith(".pdf"):
            text = ai.extract_text_from_pdf(content)
        elif file.filename.lower().endswith(".docx"):
            text = ai.extract_text_from_docx(content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Use PDF or DOCX.")
    except Exception as e:
        # Fallback error if specific extractor fails critically
        raise HTTPException(status_code=400, detail=f"Could not parse file: {str(e)}")

    if not text or len(text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Could not extract enough text from file. Maybe it's an image scan?")

    # 4. Process AI: Embedding & Similarity
    clean_text = ai.clean_text(text)
    
    # Generate embeddings (returns list of floats)
    cv_embedding = ai.get_embedding(clean_text)
    role_embedding = role.get_embedding()
    
    # Calculate score
    if not role_embedding or len(role_embedding) == 0:
        score = 0
    else:
        score = ai.calculate_similarity(cv_embedding, role_embedding)

    # 5. Explainability: Extract common keywords
    # Combine role name and description for better context matching
    role_context = f"{role.name} {role.description}"
    matched_skills = ai.extract_keywords(clean_text, role_context)

    # 6. Save Candidate
    db_candidate = models.Candidate(
        role_id=role_id,
        filename=file.filename,
        content=clean_text,
        score=score,
    )
    # cv_embedding is already a list from the new AI engine
    db_candidate.set_embedding(cv_embedding)
    db_candidate.set_matched_skills(matched_skills)
    
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    return db_candidate

@router.get("/{role_id}", response_model=List[schemas.CandidateResponse])
def get_rankings(
    role_id: int,
    db: Session = Depends(dependencies.get_db)
):
    # Retrieve candidates ordered by score desc
    candidates = db.query(models.Candidate)\
        .filter(models.Candidate.role_id == role_id)\
        .order_by(models.Candidate.score.desc())\
        .all()
    return candidates
