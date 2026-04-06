# Empire Growth OS - System Architecture

## High-Level Overview

```
PROSPECT FOUND
    ↓
LEAD CREATED (API/Import)
    ↓
N8N: Auto-Score Lead
    ↓
Score >= 8?
    ├─ YES → Harpoon AI Calls
    │         ↓
    │         Call Webhook Updates CRM
    │         ↓
    │         N8N: Send Demo Email
    │
    └─ NO → Manual Follow-up Queue

Email Sequence (Days 1, 3, 7, 14)
    ↓
Deal Closed?
    ├─ YES → Create Client
    │         ↓
    │         N8N: Onboarding
    │         ├─ Create Stripe Subscription
    │         ├─ Send Welcome Email
    │         ├─ Create Tasks
    │         └─ Deploy Chatbot
    │         ↓
    │         MONTHLY DELIVERY
    │         ├─ N8N: Google Posts
    │         ├─ N8N: Social Content
    │         ├─ Update SEO
    │         ├─ Tune Chatbot
    │         └─ Generate Report
    │
    └─ NO → Nurture List
```

## System Components

### 1. FastAPI Backend (`apps/api`)
**Responsibility:** Core data layer + API endpoints

**Routers:**
- `leads.py` - Lead CRUD + list
- `clients.py` - Client CRUD + list
- `tasks.py` - Task management
- `reports.py` - Monthly reports
- `harpoon.py` - Call webhooks + call history
- `stripe_integration.py` - Billing webhooks + MRR
- `automation.py` - Workflow triggers
- `chatbot.py` - Visitor messages + lead capture

**Database Models:**
- Lead (prospects)
- Client (paying customers)
- Task (monthly deliverables)
- Report (performance metrics)
- HarpoonCall (call logs)
- StripeSubscription (billing status)
- Invoice (payment records)
- AutomationLog (workflow execution)
- ChatbotConversation (visitor chats)

### 2. Web Dashboard (`apps/web`)
**Responsibility:** Real-time metrics + management UI

**Displays:**
- Total leads (with hot/warm/cold split)
- Active clients
- MRR (Monthly Recurring Revenue)
- Call success rate
- Conversion metrics
- Task status
- Forms to create leads

### 3. Harpoon AI Integration
**Responsibility:** Automated voice outreach

**Flow:**
```
Lead Score >= 8
    ↓
API: /api/harpoon/initiate-call
    ↓
Harpoon queues call
    ↓
Harpoon calls prospect
    ↓
Call completes
    ↓
Harpoon sends webhook
    ↓
Empire Growth OS records call
    ↓
CRM updates (lead status)
    ↓
N8N triggers next action (email)
```

**Webhook Payload:**
```json
{
  "call_id": "call_123",
  "lead_id": 42,
  "call_date": "2026-04-06T10:30:00Z",
  "duration_seconds": 180,
  "status": "completed",
  "success": true,
  "transcript": "Full call transcript...",
  "recording_url": "https://..."
}
```

### 4. Stripe Billing Integration
**Responsibility:** Recurring revenue management

**Flow:**
```
Deal Closed → Client Created
    ↓
API: /api/stripe/create-subscription
    ↓
Stripe customer created
    ↓
Subscription activated
    ↓
First invoice sent
    ↓
Payment processed
    ↓
Stripe sends webhook
    ↓
Empire Growth OS records invoice
    ↓
MRR updated
```

**MRR Calculation:**
```
MRR = SUM(monthly_price) for all active subscriptions
ARR = MRR × 12
```

**Webhook Events:**
- `customer.subscription.updated` - Status change
- `customer.subscription.deleted` - Cancellation
- `invoice.payment_succeeded` - Payment received
- `invoice.payment_failed` - Payment failed

### 5. N8N Automation
**Responsibility:** Workflow orchestration

**Workflows:**
1. Lead Import & Qualify - Batch import + auto-scoring
2. Email Sequences - Day 1, 3, 7, 14 follow-ups
3. Google Business Posts - 2-4x monthly posts
4. Lead Scoring - Real-time re-scoring
5. Client Onboarding - Setup new clients

**Trigger Types:**
- `webhook` - External API call
- `schedule` - Time-based (cron)
- `database_event` - Lead/client created/updated
- `manual` - User-triggered

### 6. Chatbot System
**Responsibility:** Website visitor engagement

**Flow:**
```
Visitor lands on client website
    ↓
Chatbot appears
    ↓
Visitor messages
    ↓
Empire Growth OS: /api/chatbot/message
    ↓
AI generates response
    ↓
Response sent to visitor
    ↓
Conversation stored
    ↓
If qualified → Convert to Lead
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   LEAD GENERATION                        │
│  Manual Entry / CSV Import / Google Search / Chatbot    │
└──────────────────┬──────────────────────────────────────┘
                   ↓
         ┌─────────────────┐
         │  Lead Database  │
         └────────┬────────┘
                  ↓
      ┌───────────────────────┐
      │ N8N: Auto-Score Lead  │
      └────────┬──────────────┘
               ↓
        Score >= 8?
       /        |
    YES        NO
     |          ↓
     |    [Warm/Cold Leads]
     |      Email Sequence
     ↓
 ┌──────────────────────┐
 │ Harpoon AI: Call     │
 └────────┬─────────────┘
          ↓
    ┌───────────────┐
    │ Call Complete │
    │ Webhook       │
    └────────┬──────┘
             ↓
    ┌─────────────────────┐
    │ CRM: Update Status  │
    │ Log Call & Transcript
    └────────┬────────────┘
             ↓
       ┌──────────────┐
       │ N8N: Email   │
       │ Sequence     │
       │ Day 1,3,7,14 │
       └─────┬────────┘
             ↓
      Deal Closed?
      /         \
    YES         NO
     |          ↓
     |    [Nurture]
     ↓
┌───────────────────────┐
│ Create Client         │
│ Stripe Subscription   │
└──────────┬────────────┘
           ↓
    ┌────────────────┐
    │ N8N Onboarding │
    ├────────────────┤
    │ • Welcome Email│
    │ • Setup Tasks  │
    │ • Deploy Chat  │
    └────────┬───────┘
             ↓
   ┌──────────────────┐
   │ MONTHLY DELIVERY │
   ├──────────────────┤
   │ • Google Posts   │
   │ • Social Content │
   │ • SEO Updates    │
   │ • Reports        │
   └────────┬─────────┘
            ↓
      ┌──────────────┐
      │ Upsell/Retain│
      └──────────────┘
```

## API Endpoint Summary

### Leads
- `POST /api/leads` - Create
- `GET /api/leads` - List all
- `GET /api/leads/{id}` - Get one
- `PUT /api/leads/{id}` - Update
- `DELETE /api/leads/{id}` - Delete

### Clients
- `POST /api/clients` - Create
- `GET /api/clients` - List all
- `GET /api/clients/{id}` - Get one

### Harpoon
- `POST /api/harpoon/webhook/call-complete` - Webhook (Harpoon → Empire)
- `POST /api/harpoon/initiate-call` - Trigger call
- `GET /api/harpoon/calls/{lead_id}` - Call history
- `GET /api/harpoon/stats` - Call metrics

### Stripe
- `POST /api/stripe/webhook/payment` - Webhook (Stripe → Empire)
- `POST /api/stripe/create-subscription` - Create subscription
- `GET /api/stripe/subscription/{client_id}` - Get subscription
- `GET /api/stripe/invoices/{client_id}` - Invoice history
- `GET /api/stripe/mrr` - Calculate MRR
- `POST /api/stripe/cancel-subscription/{client_id}` - Cancel

### Automation
- `POST /api/automation/trigger-workflow` - Trigger N8N
- `GET /api/automation/workflows` - List all
- `POST /api/automation/workflows/lead-import` - Trigger import
- `GET /api/automation/logs` - View logs

### Chatbot
- `POST /api/chatbot/message` - Handle visitor message
- `POST /api/chatbot/capture-lead` - Convert chat to lead
- `GET /api/chatbot/conversations/{client_id}` - View chats

## Integration Points

### Empire Growth OS ↔ Harpoon AI
- **Direction:** Two-way
- **Trigger:** Lead score >= 8
- **Data:** Phone, script, lead ID
- **Response:** Call status, transcript, success

### Empire Growth OS ↔ Stripe
- **Direction:** Two-way
- **Trigger:** New client or cancellation
- **Data:** Customer email, subscription tier
- **Response:** Invoice status, payment success

### Empire Growth OS ↔ N8N
- **Direction:** Two-way
- **Trigger:** API call or webhook event
- **Data:** Lead info, client data
- **Response:** Workflow status, execution logs

### Empire Growth OS ↔ Google Business
- **Direction:** One-way (outbound)
- **Trigger:** Daily at 9 AM
- **Data:** Post content, client account
- **Response:** Post published

## Security Considerations

1. **API Keys:** Store in .env, never hardcode
2. **Webhooks:** Verify signatures (Stripe, Harpoon)
3. **Database:** Use SQLite for dev, Postgres for production
4. **HTTPS:** All integrations must use HTTPS
5. **Rate Limiting:** Implement on API (future)
6. **Authentication:** Add user auth for dashboard (future)

## Scaling Path

**Phase 1 (Now):**
- SQLite database
- Single API instance
- Docker Compose

**Phase 2 (Month 2):**
- PostgreSQL database
- Multiple API instances (load balancer)
- Separate N8N instance

**Phase 3 (Month 6):**
- Kubernetes deployment
- Cloud database (RDS)
- Separate services (microservices)

## Performance Targets

- **API Response:** < 200ms
- **Lead Creation:** < 500ms
- **MRR Calculation:** < 100ms
- **Email Send:** < 1s
- **Call Initiate:** < 500ms

## Monitoring

**Key Metrics:**
- API uptime
- Lead import success rate
- Call success rate
- Email delivery rate
- Stripe payment success rate
- N8N workflow execution time
- Dashboard response time

**Alerts (implement later):**
- API down
- Webhook failures
- Payment failures
- Email delivery errors
- N8N workflow failures
