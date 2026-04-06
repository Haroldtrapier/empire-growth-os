from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True)
    business_name = Column(String, index=True)
    niche = Column(String)
    phone = Column(String)
    email = Column(String)
    website_status = Column(String)  # none, bad, good
    website_url = Column(String, nullable=True)
    google_reviews = Column(Integer, default=0)
    city = Column(String)
    contact_person = Column(String, nullable=True)
    score = Column(Integer, default=0)
    status = Column(String, default="identified")  # identified, contacted, demo_sent, proposal, won, lost
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
    package = Column(String)  # starter, growth, ai_pro
    monthly_price = Column(Float)
    status = Column(String, default="active")  # active, paused, cancelled
    contract_start = Column(DateTime)
    contract_end = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    title = Column(String)
    description = Column(Text, nullable=True)
    task_type = Column(String)  # seo, content, chatbot, social, reporting
    status = Column(String, default="pending")  # pending, in_progress, completed
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    month = Column(String)  # YYYY-MM
    leads_generated = Column(Integer, default=0)
    calls_booked = Column(Integer, default=0)
    site_visits = Column(Integer, default=0)
    form_submissions = Column(Integer, default=0)
    pages_updated = Column(Integer, default=0)
    social_posts = Column(Integer, default=0)
    report_content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)