from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models
from app.routers import roles, candidates

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Recruitment MVP", version="1.0.0")

# CORS setup
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "AI Recruitment System API is running"}

app.include_router(roles.router)
app.include_router(candidates.router)

@app.on_event("startup")
async def startup_event():
    # Seed data if empty
    from app.database import SessionLocal
    from app.services.ai_engine import AIEngine
    import json
    
    db = SessionLocal()
    role_count = 0
    try:
        role_count = db.query(models.Role).count()
    except Exception:
        # Table might not exist yet if created differently, but create_all runs above
        pass

    if role_count == 0:
        print("db is empty, creating default role...")
        ai = AIEngine() 
        
        name = "Python Backend Developer"
        description = "Looking for an expert in Python, FastAPI, SQL, and System Design."
        text = f"{name} {description}"
        embedding = ai.get_embedding(text)
        
        if hasattr(embedding, "tolist"):
            embedding = embedding.tolist()
            
        default_role = models.Role(
            name=name,
            description=description
        )
        default_role.set_embedding(embedding)
        
        db.add(default_role)
        db.commit()
        print("Default role created.")
    db.close()
