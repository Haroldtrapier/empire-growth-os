from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Lead
from app.database import get_db
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/leads", tags=["leads"])

class LeadCreate(BaseModel):
    business_name: str
    niche: str
    phone: str
    email: str
    city: str
    website_status: str = "none"
    google_reviews: int = 0

@router.get("/")
def list_leads(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()
    return {"count": len(leads), "leads": leads}

@router.post("/")
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    # Calculate score
    score = 0
    if lead.website_status == "none":
        score += 5
    elif lead.website_status == "bad":
        score += 3
    if lead.google_reviews < 20:
        score += 2
    
    db_lead = Lead(
        business_name=lead.business_name,
        niche=lead.niche,
        phone=lead.phone,
        email=lead.email,
        city=lead.city,
        website_status=lead.website_status,
        google_reviews=lead.google_reviews,
        score=score
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

@router.get("/{lead_id}")
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.put("/{lead_id}")
def update_lead(lead_id: int, lead: LeadCreate, db: Session = Depends(get_db)):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    for key, value in lead.dict().items():
        setattr(db_lead, key, value)
    
    db_lead.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_lead)
    return db_lead

@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(db_lead)
    db.commit()
    return {"deleted": True}