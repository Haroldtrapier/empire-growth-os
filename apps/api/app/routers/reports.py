from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Report
from app.database import get_db

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/{month}")
def get_report(month: str, db: Session = Depends(get_db)):
    reports = db.query(Report).filter(Report.month == month).all()
    return {"month": month, "reports": reports}