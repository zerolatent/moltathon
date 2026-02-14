# Signal-to-Site

> **Transform GTM signals into hyper-personalized outreach in 60 seconds.**

Text a company name to your OpenClaw bot. Get a branded landing page + personalized email back in under a minute.

```
You: "linear.app is hiring Head of Sales"

Agent: ✅ Done in 52 seconds!

🎨 Landing Page: https://signal-to-site.netlify.app/linear-app
   Uses Linear purple (#5E6AD2)
   References their Ramp case study

📧 Email: "Hi Karri, loved the Ramp case study—50 to 500 engineers..."

💼 LinkedIn: Ready to send (274 chars)
```

---

## What Makes This Different

This isn't template mail-merge. Signal-to-Site:

| Traditional Outreach | Signal-to-Site |
|---------------------|----------------|
| Generic templates | Pages styled in their brand colors |
| "Hi {FirstName}" | References their actual case studies |
| Manual research (30 min) | Automated research (30 sec) |
| Feels mass-produced | Feels hand-crafted |

**The magic**: We scrape their actual website, extract their brand identity, and generate assets that look like *their* team made them.

---

## Quick Start

### Prerequisites

- [OpenClaw](https://docs.openclaw.ai) installed and running
- An Anthropic API key (or other LLM provider)

### Setup (One-Time)

```bash
# Clone the repo
git clone https://github.com/moltathon/signal-to-site
cd signal-to-site

# Run setup script
./setup.sh
```

The setup script will prompt you for:
- Your API key
- Your company name & value prop
- Optional: Linkt, Netlify, Slack integrations

### Run the Demo

```bash
# Start OpenClaw
openclaw chat

# Run signal-to-site
> /signal-to-site stripe.com hiring Head of Sales
```

Or use natural language:
```
> Research linear.app and create outreach for them
```

---

## How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   INPUT     │────▶│  RESEARCH   │────▶│  GENERATE   │────▶│   OUTPUT    │
│             │     │             │     │             │     │             │
│ "linear.app │     │ Browser     │     │ Landing     │     │ Live URL    │
│  hiring     │     │ scrapes     │     │ page +      │     │ Email draft │
│  Head of    │     │ their site  │     │ outreach    │     │ LinkedIn    │
│  Sales"     │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  EXTRACTS   │
                    │             │
                    │ • Colors    │
                    │ • Tagline   │
                    │ • Team      │
                    │ • Cases     │
                    └─────────────┘
```

### The 60-Second Pipeline

1. **Parse** (2s) - Extract domain and signal from input
2. **Research** (30s) - Browser visits their site, screenshots, extracts content
3. **Analyze** (5s) - LLM identifies brand colors, tone, key hooks
4. **Generate** (20s) - Create landing page HTML + outreach drafts
5. **Deploy** (3s) - Save locally or deploy to Netlify

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed technical documentation.

---

## Features

### OpenClaw Native
- Uses OpenClaw's built-in browser automation
- Works via WhatsApp, Telegram, Discord, CLI
- Lobster workflow with approval gates
- Sub-agent support for parallel processing

### Linkt Integration
- Real GTM signals (hiring, funding, tech adoption)
- Use code **CLAW** for free credits
- Webhook support for real-time processing

### Smart Personalization
- Extracts actual brand colors from websites
- References real case studies and team members
- Matches their communication tone
- Creates landing pages in their aesthetic

### Production Ready
- Approval gates before sending
- Follow-up sequence generation
- Slack/Telegram notifications
- Netlify deployment

---

## Usage

### Slash Command

```
/signal-to-site <domain> [signal]

# Examples:
/signal-to-site stripe.com hiring Head of Sales
/signal-to-site anthropic.com raised Series C
/signal-to-site linear.app
```

### Natural Language

```
"Research acme.com and create outreach for them"
"I saw techstartup.io is hiring - build me a campaign"
"Create a personalized landing page for cloudscale.ai"
```

### With Linkt Signals

```
/signal-to-site linkt --type hiring --limit 5
```

---

## Configuration

### Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...

# Your Company (for outreach)
YOUR_COMPANY_NAME="Acme Inc"
YOUR_VALUE_PROP="AI automation that saves 10+ hours/week"
SENDER_NAME="Alex"
SENDER_EMAIL="alex@acme.com"
CTA_URL="https://calendly.com/your-link"

# Optional: Linkt
LINKT_API_KEY=your_linkt_key

# Optional: Deployment
NETLIFY_TOKEN=your_netlify_token

# Optional: Notifications
SLACK_WEBHOOK_URL=your_slack_webhook
```

### OpenClaw Config

```json
{
  "plugins": ["./path/to/signal-to-site"],
  "skills": {
    "signal-to-site": {
      "your_company": "Acme Inc",
      "your_value_prop": "AI automation",
      "sender_name": "Alex",
      "calendly_url": "https://calendly.com/demo",
      "deploy_to": "netlify",
      "auto_send": false
    }
  }
}
```

---

## Output

Generated files are saved to `./output/{domain}/`:

```
output/linear-app/
├── index.html           # Landing page (open in browser)
├── outreach.json        # Email + LinkedIn + follow-ups
├── brand-profile.json   # Research data
└── homepage.png         # Screenshot of their site
```

### Sample Landing Page

The generated page:
- Uses their exact brand colors
- Dark/light mode matching their site
- References their specific case studies
- Mentions their signal (hiring/funding)
- Includes personalized CTA

### Sample Email

```
Subject: Re: Head of Sales role

Hi Karri,

Just saw the Head of Sales posting—congrats on the growth.
The Ramp case study (50 to 500 engineers on Linear) is exactly
the kind of enterprise motion that's hard to scale without
losing the product-led magic.

We help DevTools companies like Vercel and Supabase build
sales processes that technical buyers actually respect.

Put together a quick page with some thoughts specific to Linear:
https://signal-to-site.netlify.app/linear-app

15 minutes to compare notes?

Best,
Sarah
```

---

## Project Structure

```
signal-to-site/
├── openclaw.plugin.json      # Plugin manifest
├── plugin/
│   └── index.js              # OpenClaw plugin
├── skills/
│   └── signal-to-site/
│       ├── SKILL.md          # Skill documentation
│       └── prompts/          # Agent prompts
│           ├── orchestrate.md
│           ├── research.md
│           ├── generate-page.md
│           └── generate-outreach.md
├── workflows/
│   └── signal-pipeline.yaml  # Lobster workflow
├── output/                   # Generated files
├── setup.sh                  # One-time setup
├── DEMO.md                   # Demo script
└── ARCHITECTURE.md           # Technical docs
```

---

## Demo

See [DEMO.md](DEMO.md) for a complete demo script including:
- Setup instructions
- Live demo flow
- Talking points
- Q&A prep

### Quick Demo

```bash
# 1. Start OpenClaw
openclaw chat

# 2. Run demo
> /signal-to-site linear.app hiring Head of Sales

# 3. Open generated page
open ./output/linear-app/index.html
```

---

## Hackathon Track

**SalesMolty Track** - Sponsored by Linkt AI

This project combines:
- **Linkt**: GTM signal detection (hiring, funding, tech adoption)
- **OpenClaw**: Browser automation, asset generation, multi-channel delivery

### Why This Wins

1. **Uses OpenClaw extensively** - Browser tool, Lobster workflows, sub-agents, channels
2. **Real Linkt integration** - Not mock data, actual GTM signals
3. **Visible "wow" factor** - Pages literally use their brand colors
4. **60-second demo** - Fast, impressive, memorable
5. **Production-ready** - Approval gates, error handling, deployment

---

## Links

- [Architecture Documentation](ARCHITECTURE.md)
- [Demo Script](DEMO.md)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [Linkt API](https://docs.linkt.ai)

---

## License

MIT

---

## Credits

Built for the Moltathon hackathon.

**Linkt Resources:**
- API Docs: https://docs.linkt.ai
- Free credits code: **CLAW**
- 1 month free (150 credits)
