# Empire Growth OS

AI-powered growth operating system for local businesses: websites, lead management, SEO, marketing automation, reporting, and client operations.

## Overview

Empire Growth OS is a complete system for building and managing AI-powered growth systems for local service businesses (roofing, HVAC, plumbing, etc.).

**Key Features:**
- 🚀 Fast demo website generation
- 📞 AI voice outreach via Harpoon
- 💰 Dual pricing model (one-time + recurring)
- 📊 Client CRM & pipeline management
- 🤖 AI chatbot integration
- 📈 SEO & local marketing automation
- 📋 Monthly reporting system

## Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- Python 3.10+
- Node.js 18+

### Run Locally

**With Docker (Fastest):**
```bash
docker compose up
```

Then open:
- API Docs: http://127.0.0.1:8000/docs
- Dashboard: http://127.0.0.1:8080

**Without Docker:**
```bash
# Backend
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd apps/web
python3 -m http.server 8080
```

## Project Structure

```
empire-growth-os/
├── apps/
│   ├── api/              # FastAPI backend
│   └── web/              # Web dashboard
├── automations/
│   └── n8n/              # Workflow templates
├── docs/
│   ├── implementation.md
│   ├── sales-playbook.md
│   └── operations.md
├── prompts/              # AI prompts
├── data/                 # Sample data
└── scripts/              # Utility scripts
```

## Pricing Model

### One-Time Setup
- Website build: $300–$1,000
- No monthly commitment

### Recurring (Recommended)
- Setup: $0–$300
- Monthly: $250–$450
- Minimum term: 3 months
- Then month-to-month

### Upsell Opportunities
- Advanced SEO
- Paid ads management
- Additional locations

## Next Steps

1. **Deploy API**: `docker compose up`
2. **Test Dashboard**: Open http://127.0.0.1:8080
3. **Generate Demo Sites**: Use the dashboard to create roofing/HVAC templates
4. **Configure Harpoon**: Add call scripts and voice settings
5. **Set up Stripe**: Add billing integration

## Key Workflows

### Sales Pipeline
1. Find business (Google search)
2. Build demo site
3. Harpoon AI calls
4. Send demo link + video
5. Close deal
6. Install system

### Monthly Delivery
- Website maintenance
- SEO updates
- Google Business optimization
- Social media posts
- Chatbot tuning
- Performance reports

## API Endpoints

### Leads
- `GET /api/leads` - List all leads
- `POST /api/leads` - Create new lead
- `GET /api/leads/{id}` - Get lead details
- `PUT /api/leads/{id}` - Update lead
- `DELETE /api/leads/{id}` - Delete lead

### Clients
- `GET /api/clients` - List all clients
- `POST /api/clients` - Create new client
- `GET /api/clients/{id}` - Get client details

### Tasks
- `GET /api/tasks` - List tasks
- `POST /api/tasks` - Create task

### Reports
- `GET /api/reports/{month}` - Monthly summary

## Configuration

Create `.env` file in `apps/api/`:
```
DATABASE_URL=sqlite:///./empire_growth_os.db
OPENAI_API_KEY=your_key_here
HARPOON_API_KEY=your_key_here
STRIPE_SECRET_KEY=your_key_here
```

## License

MIT

## Support

See docs/ folder for detailed guides.