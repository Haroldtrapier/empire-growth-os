from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Lead, HarpoonCall
from app.database import get_db
from pydantic import BaseModel
from datetime import datetime
import os

router = APIRouter(prefix="/api/harpoon", tags=["harpoon"])

class HarpoonWebhookPayload(BaseModel):
    call_id: str
    phone_number: str
    lead_id: int
    call_date: str
    duration_seconds: int
    status: str
    transcript: str = None
    transcript_summary: str = None
    success: bool = False
    recording_url: str = None

class CallResponse(BaseModel):
    call_id: str
    status: str

@router.post("/webhook/call-complete")
async def handle_call_complete(payload: HarpoonWebhookPayload, db: Session = Depends(get_db)):
    try:
        call = HarpoonCall(
            lead_id=payload.lead_id,
            call_id=payload.call_id,
            phone_number=payload.phone_number,
            call_date=datetime.fromisoformat(payload.call_date),
            duration_seconds=payload.duration_seconds,
            transcript=payload.transcript,
            transcript_summary=payload.transcript_summary,
            success=payload.success,
            status=payload.status,
            recording_url=payload.recording_url
        )
        
        db.add(call)
        
        lead = db.query(Lead).filter(Lead.id == payload.lead_id).first()
        if lead:
            if payload.success:
                lead.status = "demo_sent"
            elif payload.status == "no_answer":
                lead.status = "contacted"
            elif payload.status == "completed" and not payload.success:
                lead.status = "contacted"
            
            lead.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {"success": True, "call_id": payload.call_id, "lead_id": payload.lead_id}
    
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

@router.get("/calls/{lead_id}")
def get_calls_for_lead(lead_id: int, db: Session = Depends(get_db)):
    calls = db.query(HarpoonCall).filter(HarpoonCall.lead_id == lead_id).all()
    return {"lead_id": lead_id, "call_count": len(calls), "calls": calls}

@router.post("/initiate-call")
def initiate_call(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return {"lead_id": lead_id, "business_name": lead.business_name, "phone": lead.phone, "status": "queued_for_call"}

@router.get("/stats")
def get_call_stats(db: Session = Depends(get_db)):
    total_calls = db.query(HarpoonCall).count()
    successful_calls = db.query(HarpoonCall).filter(HarpoonCall.success == True).count()
    
    return {"total_calls": total_calls, "successful_calls": successful_calls, "success_rate": (successful_calls / total_calls * 100) if total_calls > 0 else 0}