from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Task
from app.database import get_db
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

class TaskCreate(BaseModel):
    client_id: int
    title: str
    task_type: str
    description: str = None
    due_date: datetime

@router.get("/")
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return {"count": len(tasks), "tasks": tasks}

@router.post("/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task