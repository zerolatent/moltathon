---
name: signal-to-site
description: >
  Transform Linkt GTM signals into hyper-personalized outreach in under 60 seconds.
  Scrapes target company websites, extracts their brand identity, generates
  landing pages that mirror their aesthetic, and crafts outreach that references
  specific details from their site. The "wow" demo: text a company name,
  get a branded landing page + personalized email in one minute.
homepage: https://github.com/moltathon/signal-to-site
user-invocable: true
---

# Signal-to-Site: Hyper-Personalized GTM Pipeline

> "Text me a company. I'll build them a landing page in their brand colors,
> referencing their actual product, in 60 seconds."

## What Makes This Different

This isn't template mail-merge. This skill:

1. **Scrapes their actual website** using OpenClaw's browser tool
2. **Extracts their brand** - colors, logo, typography, tone of voice
3. **Analyzes their product** - what they sell, who they serve, their messaging
4. **Finds specific hooks** - recent blog posts, case studies, team members
5. **Generates a landing page** that looks like THEIR design team made it
6. **Crafts outreach** that references specific things from their site

## The 60-Second Demo

```
You: "techstartup.io is hiring a Head of Marketing"

Agent: *Uses browser to visit techstartup.io*
       *Screenshots homepage, extracts brand colors (#2563eb, #1e293b)*
       *Finds their tagline: "AI-powered workflow automation"*
       *Spots case study: "How Acme Corp saved 40 hours/week"*
       *Identifies founder: Sarah Chen, CEO*

Agent: "Done! Here's what I created:

🎨 Landing Page: https://signal-to-site.netlify.app/techstartup
   - Uses their exact blue (#2563eb) as primary color
   - References their Acme Corp case study
   - Headline: "Scaling your marketing team?"

📧 Email Draft:
   Subject: Loved the Acme Corp case study

   Hi Sarah,

   Just read your case study about Acme Corp saving 40 hours/week -
   that's exactly the efficiency we help marketing teams achieve...

🔗 LinkedIn: [connection request with context]

Want me to send this or adjust anything?"
```

## How It Works

### Step 1: Signal Detection
When you mention a company + signal (hiring, funding, etc.), I detect it:
- "acme.com just raised Series A" → funding signal
- "Check out cloudscale.ai, they're hiring sales" → hiring signal
- "Research techstartup.io for outreach" → custom signal

### Step 2: Deep Website Analysis
I use OpenClaw's browser to:
```
→ Navigate to their homepage
→ Take a full-page screenshot
→ Extract all text content
→ Find their logo/brand assets
→ Visit their /about, /blog, /customers pages
→ Build a complete brand profile
```

### Step 3: Brand Extraction
From the scrape, I identify:
- **Colors**: Primary, secondary, accent (extracted from CSS/images)
- **Typography**: Their font choices and heading styles
- **Voice**: Professional? Casual? Technical? Playful?
- **Key Messages**: Taglines, value props, differentiators
- **Social Proof**: Customer logos, case studies, testimonials
- **Team**: Founders, key people with LinkedIn profiles

### Step 4: Personalized Asset Generation
I create:
- **Landing Page**: HTML/CSS that mirrors their brand aesthetic
- **Email**: References specific content from their site
- **LinkedIn Message**: Mentions something only someone who read their site would know
- **Follow-up Sequence**: 3-touch campaign with increasing specificity

### Step 5: Deployment & Delivery
- Page deployed to Netlify/Vercel (live URL in seconds)
- Email ready to send (or auto-send if approved)
- Everything logged for tracking

## Commands

### Natural Language (Recommended)
Just talk to me:
- "Research acme.com and create outreach for them"
- "I saw techstartup.io is hiring - build me a campaign"
- "Create a personalized landing page for cloudscale.ai"

### Slash Commands
```
/signal-to-site <domain> [signal]
/signal-to-site techstartup.io "hiring Head of Marketing"
/signal-to-site acme.com "raised Series A"
```

### With Linkt Integration
```
/signal-to-site linkt --type hiring --limit 3
```
Fetches real signals from Linkt and processes each one.

## What Gets Created

### The Landing Page
Not a generic template. A page that:
- Uses THEIR color palette
- Matches THEIR typography style
- References THEIR specific use case
- Shows understanding of THEIR industry
- Includes THEIR company name prominently
- Has a CTA relevant to THEIR situation

### The Email
Not "Dear {FirstName}". An email that:
- Opens with something specific from their website
- References a real case study, blog post, or product feature
- Connects their situation (hiring/funding) to your solution
- Feels like you actually researched them (because we did)

### The LinkedIn Message
Short, specific, impossible to ignore:
- Mentions something only a real researcher would find
- Connects on shared context
- No generic "I'd love to connect"

## Configuration

Set in your OpenClaw config or via environment:

```json
{
  "skills": {
    "signal-to-site": {
      "your_company": "Acme Inc",
      "your_value_prop": "AI automation that saves 10+ hours/week",
      "sender_name": "Alex",
      "sender_email": "alex@acme.com",
      "calendly_url": "https://calendly.com/alex-acme",
      "deploy_to": "netlify",
      "netlify_token": "...",
      "auto_send": false
    }
  }
}
```

## Pro Tips

### For the Demo
1. Pick a real company with a good website (more to extract)
2. Use a hiring signal (most actionable)
3. Show the live page loading in browser
4. Point out specific personalization ("see how it uses their blue?")

### For Real Usage
1. Start with `auto_send: false` to review first
2. Use Linkt signals for warm leads
3. Track which personalizations get responses
4. Iterate on your value prop based on what resonates

## The Wow Factor

This isn't just automation. It's **research that would take 30 minutes, done in 60 seconds**.

The landing page doesn't look templated because it isn't - it's dynamically styled based on their actual brand. The email doesn't feel generic because it references their actual content.

**That's the demo moment**: Show a judge's company, generate a page in their brand colors referencing their real case studies, in under a minute. They'll remember that.
