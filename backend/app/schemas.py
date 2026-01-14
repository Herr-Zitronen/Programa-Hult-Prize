from pydantic import BaseModel
from typing import List, Optional

class RoleBase(BaseModel):
    name: str
    description: str

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int
    
    class Config:
        from_attributes = True

class CandidateResponse(BaseModel):
    id: int
    role_id: int
    filename: str
    score: int
    matched_skills: List[str]

    class Config:
        from_attributes = True
