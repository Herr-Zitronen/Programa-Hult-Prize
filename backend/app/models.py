from sqlalchemy import Column, Integer, String, Text, LargeBinary
from .database import Base
import json

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    # Storing embedding as a JSON string for simplicity in SQLite
    embedding_json = Column(Text)

    def set_embedding(self, embedding_list):
        self.embedding_json = json.dumps(embedding_list)

    def get_embedding(self):
        if not self.embedding_json:
            return []
        return json.loads(self.embedding_json)

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, index=True)
    filename = Column(String)
    content = Column(Text)  # The extracted text
    score = Column(Integer) # 0-100
    matched_skills_json = Column(Text) # JSON list of matched skills
    embedding_json = Column(Text)

    def set_embedding(self, embedding_list):
        self.embedding_json = json.dumps(embedding_list)

    def get_embedding(self):
        if not self.embedding_json:
            return []
        return json.loads(self.embedding_json)

    def set_matched_skills(self, skills_list):
        self.matched_skills_json = json.dumps(skills_list)
    
    @property
    def matched_skills(self):
        if not self.matched_skills_json:
            return []
        return json.loads(self.matched_skills_json)
