from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Client, StripeSubscription, Invoice
from app.database import get_db
from pydantic import BaseModel
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/api/stripe", tags=["stripe"])

class CreateSubscriptionRequest(BaseModel):
    client_id: int
    package: str
    setup_fee: float = 0

pricing_tiers = {"starter": 150, "growth": 300, "ai_pro": 500}

@router.post("/webhook/payment")
async def handle_stripe_webhook(request_body: dict, db: Session = Depends(get_db)):
    event_type = request_body.get("type")
    data = request_body.get("data", {}).get("object", {})
    
    try:
        if event_type == "customer.subscription.updated":
            subscription_id = data.get("id")
            status = data.get("status")
            subscription = db.query(StripeSubscription).filter(StripeSubscription.stripe_subscription_id == subscription_id).first()
            if subscription:
                subscription.status = status
                subscription.updated_at = datetime.utcnow()
                db.commit()
        
        elif event_type == "customer.subscription.deleted":
            subscription_id = data.get("id")
            subscription = db.query(StripeSubscription).filter(StripeSubscription.stripe_subscription_id == subscription_id).first()
            if subscription:
                subscription.status = "canceled"
                subscription.cancellation_date = datetime.utcnow()
                subscription.updated_at = datetime.utcnow()
                db.commit()
        
        elif event_type == "invoice.payment_succeeded":
            invoice_id = data.get("id")
            customer_id = data.get("customer")
            amount = data.get("amount_paid") / 100
            subscription = db.query(StripeSubscription).filter(StripeSubscription.stripe_customer_id == customer_id).first()
            if subscription:
                invoice = Invoice(
                    client_id=subscription.client_id,
                    stripe_invoice_id=invoice_id,
                    amount=amount,
                    status="paid",
                    period_start=datetime.utcnow(),
                    period_end=datetime.utcnow() + timedelta(days=30),
                    due_date=datetime.utcnow() + timedelta(days=30),
                    paid_date=datetime.utcnow(),
                    invoice_url=data.get("hosted_invoice_url")
                )
                db.add(invoice)
                db.commit()
        
        return {"status": "success", "event": event_type}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/create-subscription")
def create_subscription(req: CreateSubscriptionRequest, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == req.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    monthly_price = pricing_tiers.get(req.package, 300)
    subscription = StripeSubscription(
        client_id=req.client_id,
        stripe_customer_id=f"cus_{req.client_id}",
        stripe_subscription_id=f"sub_{req.client_id}",
        status="active",
        current_period_start=datetime.utcnow(),
        current_period_end=datetime.utcnow() + timedelta(days=30),
        amount_monthly=monthly_price,
        setup_fee=req.setup_fee,
        setup_fee_paid=req.setup_fee == 0
    )
    
    db.add(subscription)
    client.stripe_customer_id = subscription.stripe_customer_id
    client.stripe_subscription_id = subscription.stripe_subscription_id
    db.commit()
    
    return {"success": True, "client_id": req.client_id, "subscription_id": subscription.stripe_subscription_id, "monthly_price": monthly_price}

@router.get("/subscription/{client_id}")
def get_subscription(client_id: int, db: Session = Depends(get_db)):
    subscription = db.query(StripeSubscription).filter(StripeSubscription.client_id == client_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

@router.get("/invoices/{client_id}")
def get_invoices(client_id: int, db: Session = Depends(get_db)):
    invoices = db.query(Invoice).filter(Invoice.client_id == client_id).all()
    return {"client_id": client_id, "invoice_count": len(invoices), "invoices": invoices}

@router.get("/mrr")
def get_mrr(db: Session = Depends(get_db)):
    subscriptions = db.query(StripeSubscription).filter(StripeSubscription.status == "active").all()
    total_mrr = sum(sub.amount_monthly for sub in subscriptions)
    return {"total_mrr": total_mrr, "active_subscriptions": len(subscriptions), "mrr_by_tier": {"starter": sum(s.amount_monthly for s in subscriptions if s.amount_monthly == 150), "growth": sum(s.amount_monthly for s in subscriptions if s.amount_monthly == 300), "ai_pro": sum(s.amount_monthly for s in subscriptions if s.amount_monthly == 500)}}

@router.post("/cancel-subscription/{client_id}")
def cancel_subscription(client_id: int, reason: str = "", db: Session = Depends(get_db)):
    subscription = db.query(StripeSubscription).filter(StripeSubscription.client_id == client_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription.status = "canceled"
    subscription.cancellation_date = datetime.utcnow()
    subscription.cancellation_reason = reason
    subscription.updated_at = datetime.utcnow()
    db.commit()
    return {"success": True, "message": f"Subscription canceled for client {client_id}"}