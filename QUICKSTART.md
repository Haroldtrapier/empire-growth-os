# Empire Growth OS - Full System Quick Start

## What You Have
- ✅ FastAPI backend (leads, clients, tasks, reports)
- ✅ Web dashboard (real-time metrics)
- ✅ Harpoon AI integration (automated calling)
- ✅ Stripe billing (recurring subscriptions)
- ✅ N8N automation (email, Google Business, lead scoring)
- ✅ Chatbot system (AI visitor capture)

## Setup (15 minutes)

### 1. Clone and Configure
```bash
cd empire-growth-os
cp .env.example .env

# Edit .env with your credentials:
# - HARPOON_API_KEY
# - STRIPE_SECRET_KEY
# - SMTP settings (Gmail or SendGrid)
```

### 2. Start Everything
```bash
docker compose -f docker-compose-full.yml up
```

This starts:
- API: http://127.0.0.1:8000 (with docs at /docs)
- Dashboard: http://127.0.0.1:8080
- N8N: http://127.0.0.1:5678 (username: admin, password: changeme)
- Postgres: localhost:5432

### 3. First Steps

**Create a lead:**
```bash
curl -X POST http://localhost:8000/api/leads \
  -H "Content-Type: application/json" \
  -d '{"business_name": "ABC Roofing", "niche": "roofing", "phone": "+17041234567", "email": "info@abcroofing.com", "city": "Charlotte", "website_status": "none"}'
```

**Create a client:**
```bash
curl -X POST http://localhost:8000/api/clients \
  -H "Content-Type: application/json" \
  -d '{"business_name": "ABC Roofing", "niche": "roofing", "phone": "+17041234567", "email": "info@abcroofing.com", "city": "Charlotte", "services": "Roof repair", "package": "growth", "monthly_price": 300}'
```

**Create Stripe subscription:**
```bash
curl -X POST http://localhost:8000/api/stripe/create-subscription \
  -H "Content-Type: application/json" \
  -d '{"client_id": 1, "package": "growth", "setup_fee": 300}'
```

**Check MRR:**
```bash
curl http://localhost:8000/api/stripe/mrr
```

**Queue a call:**
```bash
curl -X POST http://localhost:8000/api/harpoon/initiate-call \
  -H "Content-Type: application/json" \
  -d '{"lead_id": 1}'
```

## Full Workflow

1. Lead created → Auto-scored
2. Hot leads → Harpoon calls
3. Call completes → Demo email sent
4. Email sequence → Day 1, 3, 7, 14
5. Deal closed → Stripe subscription
6. Client active → Monthly deliverables
7. Monthly → Google posts, social, reports

## See docs/ for detailed setup:
- `harpoon-setup.md` - Calling system
- `stripe-setup.md` - Billing
- `n8n-setup.md` - Automation

**You now have a complete growth system. Time to close deals. 🚀**