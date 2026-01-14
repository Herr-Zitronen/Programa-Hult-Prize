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
    # ai dependency removed from usage, but kept if needed for signature compatibility, though not used here.
    # actually better to just not use it.
):
    # 1. Create Role object directly
    db_role = models.Role(name=role.name, description=role.description)
    
    # 2. Logic NLP doesn't use embeddings, pass empty list
    db_role.set_embedding([])
    
    # 3. Save to DB with error handling
    try:
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating role. Title might be duplicate. {str(e)}")
    
    return db_role

@router.get("/", response_model=List[schemas.RoleResponse])
def read_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(dependencies.get_db)
):
    roles = db.query(models.Role).offset(skip).limit(limit).all()
    return roles

@router.delete("/{role_id}")
def delete_role(
    role_id: int,
    db: Session = Depends(dependencies.get_db)
):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db.delete(role)
    db.commit()
    return {"message": "Role deleted"}
