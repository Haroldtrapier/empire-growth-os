import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from app.models import Base, Lead, Client, Task, Report
from app.database import get_db
from app.routers import leads, clients, tasks, reports

# Initialize FastAPI
app = FastAPI(
    title="Empire Growth OS API",
    description="AI-powered growth system for local businesses",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./empire_growth_os.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Routes
app.include_router(leads.router)
app.include_router(clients.router)
app.include_router(tasks.router)
app.include_router(reports.router)

@app.get("/")
async def root():
    return {
        "name": "Empire Growth OS API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)