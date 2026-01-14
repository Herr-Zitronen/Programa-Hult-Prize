from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, dependencies
from ..services.ai_engine import AIEngine

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.RoleResponse)
def create_role(
    role: schemas.RoleCreate,
    db: Session = Depends(dependencies.get_db),
    ai: AIEngine = Depends(dependencies.get_ai_engine)
):
    # 1. Generate text for embedding (Title + Description)
    full_text = f"{role.name} {role.description}"
    
    # 2. Generate embedding
    embedding = ai.get_embedding(full_text)
    
    # 3. Create Role object
    db_role = models.Role(name=role.name, description=role.description)
    
    # 4. Save embedding (as list/JSON)
    # Convert numpy array to list if needed
    if hasattr(embedding, "tolist"):
        embedding = embedding.tolist()
    db_role.set_embedding(embedding)
    
    # 5. Save to DB
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    
    return db_role

@router.get("/", response_model=List[schemas.RoleResponse])
def read_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(dependencies.get_db)
):
    roles = db.query(models.Role).offset(skip).limit(limit).all()
    return roles
