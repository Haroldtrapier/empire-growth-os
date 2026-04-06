from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# ============= EXISTING MODELS =============
class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True)
    business_name = Column(String, index=True)
    niche = Column(String)
    phone = Column(String)
    email = Column(String)
    website_status = Column(String)
    website_url = Column(String, nullable=True)
    google_reviews = Column(Integer, default=0)
    city = Column(String)
    contact_person = Column(String, nullable=True)
    score = Column(Integer, default=0)
    status = Column(String, default="identified")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    business_name = Column(String, index=True)
    niche = Column(String)
    phone = Column(String)
    email = Column(String)
    city = Column(String)
    website_url = Column(String, nullable=True)
    services = Column(Text)
    package = Column(String)
    monthly_price = Column(Float)
    status = Column(String, default="active")
    contract_start = Column(DateTime)
    contract_end = Column(DateTime, nullable=True)
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    title = Column(String)
    description = Column(Text, nullable=True)
    task_type = Column(String)
    status = Column(String, default="pending")
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    month = Column(String)
    leads_generated = Column(Integer, default=0)
    calls_booked = Column(Integer, default=0)
    site_visits = Column(Integer, default=0)
    form_submissions = Column(Integer, default=0)
    pages_updated = Column(Integer, default=0)
    social_posts = Column(Integer, default=0)
    report_content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# ============= NEW MODELS FOR INTEGRATIONS =============

class HarpoonCall(Base):
    __tablename__ = "harpoon_calls"
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, index=True)
    call_id = Column(String, unique=True)
    phone_number = Column(String)
    call_date = Column(DateTime)
    duration_seconds = Column(Integer, default=0)
    transcript = Column(Text, nullable=True)
    transcript_summary = Column(Text, nullable=True)
    success = Column(Boolean, default=False)
    status = Column(String)
    notes = Column(Text, nullable=True)
    recording_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class StripeSubscription(Base):
    __tablename__ = "stripe_subscriptions"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, index=True)
    stripe_customer_id = Column(String, unique=True)
    stripe_subscription_id = Column(String, unique=True, nullable=True)
    status = Column(String)
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    amount_monthly = Column(Float)
    setup_fee = Column(Float, default=0)
    setup_fee_paid = Column(Boolean, default=False)
    cancellation_date = Column(DateTime, nullable=True)
    cancellation_reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    stripe_invoice_id = Column(String, nullable=True)
    amount = Column(Float)
    status = Column(String)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    due_date = Column(DateTime)
    paid_date = Column(DateTime, nullable=True)
    invoice_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AutomationLog(Base):
    __tablename__ = "automation_logs"
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, nullable=True)
    client_id = Column(Integer, nullable=True)
    workflow_name = Column(String)
    action = Column(String)
    metadata = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatbotConversation(Base):
    __tablename__ = "chatbot_conversations"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    visitor_id = Column(String)
    visitor_name = Column(String, nullable=True)
    visitor_email = Column(String, nullable=True)
    visitor_phone = Column(String, nullable=True)
    messages = Column(JSON)
    lead_created = Column(Boolean, default=False)
    lead_id = Column(Integer, nullable=True)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)