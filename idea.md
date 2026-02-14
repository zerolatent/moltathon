# Moltathon Ideas - Stack Ranked by Impact

## Tier 1: High Impact + High Winnability

### 1. Smart Model Router Skill
**Track:** Skillsmaxxing
**Impact:** Very High

Build a skill that analyzes incoming tasks and routes them to the cheapest capable model. Simple tasks go to cheaper/faster models, complex ones to more powerful models.

**Why it wins:**
- Direct cost savings (measurable ROI)
- Solves a real pain point for anyone running agents at scale
- Can show before/after cost comparisons in demo
- Relatively contained scope

**Bonus:** Stack with "Best Skill" side quest

---

### 2. Invoice Processing Agent
**Track:** Automate Your Life
**Impact:** Very High

Watches Gmail for invoices, extracts line items via OCR/parsing, logs to spreadsheet, sends daily summary to phone.

**Why it wins:**
- Solves real pain (everyone hates invoice management)
- Tangible demo: show real invoices getting processed
- End-to-end automation is impressive
- Personal story angle (how much time it saves you)

---

### 3. One-Click Deploy to Railway/Fly.io
**Track:** Best Deployment Tool
**Impact:** High

Create a "Deploy to Railway" or "Deploy to Fly.io" button template with sensible defaults. Include environment variable setup and channel pairing wizard.

**Why it wins:**
- Literally measures success by simplicity
- Low barrier to implement well
- Benefits entire ecosystem (judges love community impact)
- Can demo in < 2 minutes

**Bonus:** Stack with "Platform / Product Molts" side quest

---

## Tier 2: High Impact, Moderate Complexity

### 4. GTM Signal-to-Outreach Pipeline (Linkt Integration)
**Track:** SalesMolty Track w/ Linkt AI
**Impact:** High

Use Linkt to find companies with hiring signals, then auto-generate personalized landing pages and outreach sequences.

**Why it wins:**
- Sponsored track = potentially less competition
- Free Linkt credits lower dev costs
- Clear demo flow: signal detected → action taken
- Real business value (pipeline generation)

---

### 5. Context Compression Skill
**Track:** Skillsmaxxing
**Impact:** High

Summarizes conversation history when context gets long, preserving critical info while dramatically cutting tokens.

**Why it wins:**
- Measurable impact (token savings, cost reduction)
- Every long-running agent needs this
- Can benchmark quality preservation vs token savings
- Technical depth impresses judges

**Bonus:** Stack with "Best Skill" side quest

---

### 6. Meeting Prep Agent
**Track:** Automate Your Life
**Impact:** Medium-High

Cron job checks calendar each morning, researches attendees (LinkedIn, company info), texts briefing to your phone.

**Why it wins:**
- Relatable use case (everyone has meetings)
- Clear before/after: "I used to spend 15 min prepping, now it's done for me"
- Daily utility makes it feel real

---

## Tier 3: Moderate Impact, Fun Factor

### 7. Retry/Fallback Skill
**Track:** Skillsmaxxing
**Impact:** Medium

Catches API failures, rate limits, and errors then intelligently retries with different providers or strategies.

**Why it wins:**
- Production-grade feel
- Every agent deployment needs this
- Can demo failure scenarios and recovery

---

### 8. Web-Based Setup Wizard
**Track:** Best Deployment Tool
**Impact:** Medium

A simple web UI that walks you through OpenClaw setup and generates `openclaw.json`.

**Why it wins:**
- Visual demo
- "Grandma test" alignment
- Lower technical bar but polished UX wins

---

### 9. Something Hilarious (IoT + Agent)
**Track:** Make Me Laugh + Best Rig
**Impact:** Variable

Example: Agent that roasts you when you open the fridge too many times. Or a "passive aggressive assistant" that complies but judges you.

**Why it wins:**
- Memorable demo
- Double side quest eligibility
- Judges remember funny hacks
- Differentiation from serious projects

---

---

## Deep Dive: GTM Signal-to-Outreach Pipeline

### The Winning Concept: "Signal-to-Site"

**One-liner:** When Linkt detects a hiring signal, OpenClaw auto-generates a personalized landing page and sends multi-channel outreach within minutes.

### How It Works

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   LINKT LAYER   │────▶│  OPENCLAW AGENT │────▶│     OUTPUT      │
│                 │     │                 │     │                 │
│ • Hiring signal │     │ • Research co.  │     │ • Custom page   │
│ • Funding round │     │ • Generate copy │     │ • Email draft   │
│ • Tech adoption │     │ • Build assets  │     │ • LinkedIn msg  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Specific Flow (Demo-Ready)

1. **Signal Detection (Linkt)**
   - ICP: "B2B SaaS companies in Austin, 20-100 employees"
   - Signal: "Just posted first Sales/Marketing hire"

2. **Research Phase (OpenClaw)**
   - Scrape company website for value props, industry, tone
   - Find founder LinkedIn profiles
   - Identify their likely pain points based on role hired

3. **Asset Generation (OpenClaw)**
   - Generate personalized landing page showing:
     - "How [Your Product] helps teams like [Company Name]"
     - Industry-specific case study snippet
     - Custom CTA: "See how we helped [Similar Company] scale"
   - Deploy to Vercel/Netlify with unique URL

4. **Outreach Execution (OpenClaw)**
   - Draft personalized email referencing the hire
   - Draft LinkedIn connection request with context
   - Log everything to a CRM sheet
   - Send summary to Slack/Telegram

### Why This Concept Wins

| Factor | Why It's Strong |
|--------|-----------------|
| **Demo Impact** | Live signal → live page in < 2 min |
| **Measurable** | "Generated 50 personalized pages, 12 responses" |
| **Full Stack** | Shows Linkt + OpenClaw working end-to-end |
| **Real Value** | GTM teams actually want this |
| **Sponsored Track** | Less competition, dedicated judges |

### Tech Stack Suggestion

- **Linkt SDK** - Signal detection + company enrichment
- **OpenClaw** - Orchestration + browser automation
- **Vercel/Netlify** - Landing page hosting (free tier)
- **Simple HTML template** - Fast page generation
- **Gmail API or SMTP** - Outreach delivery
- **Slack/Telegram** - Notifications

### MVP Scope (Hackathon-Sized)

**Must Have:**
- Linkt → detect 1 signal type (hiring)
- Generate 1 landing page template with dynamic content
- Send 1 outreach channel (email OR LinkedIn)

**Nice to Have:**
- Multiple signal types
- A/B test different page templates
- Multi-channel outreach
- Analytics dashboard

### Demo Script (2 min)

1. "Here's my ICP in Linkt: Austin startups hiring marketers"
2. "Linkt just detected Company X posted a marketing role"
3. "Watch OpenClaw research them..." (show browser automation)
4. "Page generated: companyX.yoursite.com" (show live page)
5. "Email drafted and sent, logged to sheet"
6. "I woke up to 3 replies this morning"

### Differentiation Ideas

- **Industry vertical:** Focus on one niche (e.g., "for recruiting agencies" or "for dev tools")
- **Speed flex:** Show page generation in <60 seconds
- **Quality flex:** Show the page actually looks good, not generic
- **Results flex:** Run it for real before the demo, show actual replies

---

## Recommendation

**If going for the win:** Pick #1 (Smart Model Router) or #2 (Invoice Agent) + stack a side quest.

**If limited time:** Pick #3 (One-Click Deploy) — smallest scope, high impact.

**If want sponsored prize:** Pick #4 (Linkt GTM Pipeline) — less competition, dedicated prize pool.

**If want to stand out:** Pick #9 (Funny Rig) — memorable demos win hearts.
