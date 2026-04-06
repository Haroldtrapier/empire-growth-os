from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Client
from app.database import get_db
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/clients", tags=["clients"])

class ClientCreate(BaseModel):
    business_name: str
    niche: str
    phone: str
    email: str
    city: str
    services: str
    package: str
    monthly_price: float

@router.get("/")
def list_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return {"count": len(clients), "clients": clients}

@router.post("/")
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = Client(
        business_name=client.business_name,
        niche=client.niche,
        phone=client.phone,
        email=client.email,
        city=client.city,
        services=client.services,
        package=client.package,
        monthly_price=client.monthly_price,
        contract_start=datetime.utcnow()
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/{client_id}")
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}")
def update_client(client_id: int, client: ClientCreate, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    for key, value in client.dict().items():
        setattr(db_client, key, value)
    
    db_client.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_client)
    return db_client

@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(db_client)
    db.commit()
    return {"deleted": True}