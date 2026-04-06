# N8N Automation Workflows

## Overview
Five core workflows run all your automations:

1. **Lead Import & Auto-Qualify** - CSV to leads, auto-score
2. **Email Follow-up Sequence** - Day 1, 3, 7, 14 emails
3. **Google Business Posts** - 2-4x monthly auto-posts
4. **Lead Scoring** - Real-time scoring on creation
5. **Client Onboarding** - Auto-setup new clients

## 1. Lead Import & Auto-Qualify

**When it runs:** Manual or scheduled
**Input:** CSV or API call with leads
**Output:** Leads created, scored, hot leads queued for calls

**Example input:**
```json
{
  "leads": [
    {
      "name": "ABC Roofing",
      "phone": "+17041234567",
      "email": "info@abcroofing.com",
      "city": "Charlotte",
      "niche": "roofing"
    }
  ]
}
```

**Trigger it:**
```bash
curl -X POST http://localhost:8000/api/automation/workflows/lead-import \
  -H "Content-Type: application/json" \
  -d '{"leads": [{"name": "ABC", "phone": "+1234567890", "email": "test@test.com", "city": "Charlotte", "niche": "roofing"}]}'
```

## 2. Email Follow-up Sequence

**When it runs:** When lead status = "contacted"
**Pattern:** Day 1, 3, 7, 14

**Day 1 Email:**
```
Subject: Your {{business_name}} Website Preview

Hi {{contact_name}},

I put together a quick website showing how {{business_name}} could get more customers.
Here's your preview: {{demo_site_url}}

Best,
[Your Name]
```

**Day 3 Email:**
```
Subject: Did you see your preview?

Hi {{contact_name}},

Just checking - did you get a chance to look at your preview?
If you have questions, I'm here.

Best
```

**Day 7 Email:**
```
Subject: Last spot available

Hi {{contact_name}},

We're filling our roster for {{month}}.
You still have a spot if you want it.
```

**Day 14 Email:**
```
Subject: Final opportunity

Hi {{contact_name}},

This is my last outreach.
If you want to move forward, let me know.
Otherwise, I'll assume you're set.
```

## 3. Google Business Posts

**When it runs:** Daily at 9 AM (posts on 1st, 8th, 15th, 22nd)
**Posts per month:** 4
**Type:** Variety of topics

**Example posts:**
```
Project Showcase:
"Just finished a full roof replacement for a home on Main St.
Looking great! Questions about your roof? We're here to help."

Seasonal Tips:
"Spring Roof Maintenance Checklist:
✓ Check for winter damage
✓ Clean gutters
✓ Inspect flashing
✓ Trim branches

Give us a call!"

Review Feature:
"Thank you {{reviewer_name}} for the 5-star review!
'Fast, professional, and fair pricing.' That's what we strive for."

Team Highlight:
"Meet our team lead, John! 15 years of roofing experience.
Always puts customers first. Give us a call for expert service."
```

## 4. Lead Scoring

**When it runs:** Real-time on new lead
**Scoring logic:**
```
No website: +5 points
Bad website: +3 points
<20 reviews: +2 points
High-value niche: +1 point
─────────────────────
Score >= 8? Auto-call
Score 5-7? Warm lead
Score < 5? Cold lead
```

**Scoring tiers:**
- **Hot (8+):** Auto-queued for Harpoon call immediately
- **Warm (5-7):** Manual outreach or email sequence
- **Cold (<5):** Add to nurture list

**Trigger manually:**
```bash
curl -X POST http://localhost:8000/api/automation/workflows/lead-qualification
```

## 5. Client Onboarding

**When it runs:** When client is created (deal closed)
**Steps:**
1. Send welcome email
2. Create Stripe subscription
3. Create initial task list
4. Send onboarding checklist

**Tasks created:**
- Day 1: Set up website hosting
- Day 3: Optimize Google Business Profile
- Day 5: Create content calendar
- Day 7: Deploy chatbot

**Onboarding email:**
```
Subject: Welcome to Empire Growth OS!

Hi {{contact_name}},

Welcome to the team! We're excited to help {{business_name}} grow.

Here's what happens now:
✓ Website goes live this week
✓ Google Business optimized
✓ AI chatbot deployed
✓ Monthly content calendar

Your dashboard: {{client_portal_url}}
Questions? {{support_email}}

Let's grow together!
```

## Monitoring Workflows

**View all automation logs:**
```bash
curl http://localhost:8000/api/automation/logs
```

**View specific workflow logs:**
```bash
curl http://localhost:8000/api/automation/logs/lead_import
curl http://localhost:8000/api/automation/logs/email_sequence
curl http://localhost:8000/api/automation/logs/google_business_post
```

**Response format:**
```json
{
  "workflow": "email_sequence",
  "log_count": 142,
  "logs": [
    {
      "id": 1,
      "lead_id": 42,
      "workflow_name": "email_sequence",
      "action": "completed",
      "metadata": {"email_day": 1},
      "created_at": "2026-04-06T10:30:00Z"
    }
  ]
}
```

## Scheduling

**Lead Import:**
- Manual OR Daily at 8 AM

**Lead Scoring:**
- Real-time (on lead.created)

**Email Sequences:**
- Real-time (on lead.contacted)

**Google Business Posts:**
- Daily at 9 AM

**Client Onboarding:**
- Real-time (on client.created)

## Troubleshooting

**Workflow not triggering:**
1. Check trigger condition matches
2. Verify webhook URL is correct
3. Check N8N execution logs

**Email not sending:**
1. Verify SMTP credentials in .env
2. Check email template has required fields
3. Test with simpler email

**Google posts not posting:**
1. Verify Google API credentials
2. Check client has Google Business account
3. Test with manual post first

**Lead not auto-calling:**
1. Check score >= 8
2. Verify Harpoon API key
3. Check Harpoon account has credits

## Next Steps

1. Deploy workflows to N8N
2. Test each with sample data
3. Enable real data flow
4. Monitor first week
5. Optimize based on results
