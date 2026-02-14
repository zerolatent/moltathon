# Signal-to-Site: Demo Script

## The Pitch (30 seconds)

> "What if you could turn a Linkt signal into a personalized landing page in under 60 seconds?"
>
> "Not template mail-merge. A page that uses their exact brand colors, references their actual case studies, and feels like you spent 30 minutes researching them."
>
> "Let me show you."

## Live Demo Flow (2 minutes)

### Setup (before demo)
1. Have OpenClaw running with the plugin installed
2. Have WhatsApp/Telegram connected (for wow factor)
3. Pick a real company with a good website (stripe.com, linear.app, etc.)
4. Have their website open in a tab for comparison

### The Demo

**Step 1: The Trigger** (10 seconds)

On your phone/WhatsApp (if connected):
```
You: stripe.com is hiring a Head of Partnerships
```

Or via command line:
```
/signal-to-site stripe.com hiring Head of Partnerships
```

**Step 2: Watch the Magic** (45 seconds)

The agent will:
1. "🔍 Researching stripe.com..."
2. [Browser opens, navigates to stripe.com]
3. [Screenshot appears]
4. "Found: 'Financial infrastructure for the internet'"
5. "Primary color: #635BFF (Stripe purple)"
6. "Checking about page..."
7. "Found case study: Shopify processes $billions"
8. "Generating personalized assets..."

**Step 3: The Reveal** (30 seconds)

```
✅ Done in 52 seconds!

🎨 Landing Page: ./output/stripe-com/index.html
   Colors: #635BFF (Stripe purple)
   Headline: "Scaling your Partnerships team at Stripe?"
   Hook: References Shopify case study

📧 Email Draft:
   Subject: Re: Head of Partnerships role

   Hi [Founder],

   Just read the Shopify case study - processing $444B in 2023 is
   remarkable. As you scale the partnerships team, the challenge is
   usually finding people who understand both technical integration
   and business development.

   We help companies like [similar company] build partnership programs
   that drive revenue. Happy to share what's worked.

   15 mins to compare notes?

   Best,
   Alex

💼 LinkedIn (292 chars):
   "Hi, loved the Shopify case study - $444B processed is wild.
   Given you're scaling partnerships, thought I might be able to help.
   We work with similar API-first companies. Would love to connect."
```

**Step 4: The Proof** (15 seconds)

Open the generated page. Point out:
- "See the purple? That's #635BFF - Stripe's exact brand color"
- "The headline mentions their partnerships team"
- "It references the Shopify case study I found on their site"
- "This took 52 seconds, not 30 minutes"

### Demo Script Lines

**Opening:**
"Every GTM team spends hours researching prospects before reaching out. What if an AI could do that research AND create the assets in under a minute?"

**During research:**
"Watch the browser - it's visiting their site, extracting content, finding specific hooks..."

**After reveal:**
"The landing page isn't templated - it literally uses their brand colors. The email references a real case study from their website. This feels personalized because it IS personalized."

**Closing:**
"Linkt tells you WHO to reach out to. Signal-to-Site tells you HOW - with assets that feel like you spent 30 minutes on each one."

## Backup Demo (if live fails)

If browser automation is slow or fails, show pre-generated output:

1. Show `output/stripe-com/homepage.png` - "Here's what the agent saw"
2. Show `output/stripe-com/index.html` - "Here's the page it generated"
3. Show `output/stripe-com/outreach.json` - "Here's the email it drafted"

The story is the same: real research → real personalization → real results.

## Q&A Prep

**Q: How accurate is the brand extraction?**
A: We're not pixel-perfect - but we're getting primary colors, tone, and key messages right. The point is to feel researched, not to pass a brand audit.

**Q: Does this actually work with Linkt?**
A: Yes! Linkt provides the signals (who's hiring, who raised), we handle the outreach generation. It's a complete pipeline.

**Q: What about rate limiting / getting blocked?**
A: We're visiting public pages like any user would. For high volume, you'd want to add delays - but for targeted outreach, this isn't a concern.

**Q: Can it actually send emails?**
A: Yes, with an approval gate. We never auto-send - human reviews everything first.

## Technical Differentiators to Mention

1. **OpenClaw Native**: Uses browser tool, not a separate Playwright setup
2. **Lobster Workflow**: Deterministic pipeline with approval gates
3. **Sub-agent Architecture**: Could process 10 signals in parallel
4. **Multi-channel**: Works via WhatsApp, Telegram, Discord, CLI
5. **Linkt Integration**: Real GTM signals, not made-up data

## The "Wow" Checklist

Before the demo, verify:
- [ ] OpenClaw is running
- [ ] Plugin is installed (`openclaw plugins list`)
- [ ] Browser tool is available
- [ ] Target website loads fast
- [ ] You've tested this exact flow once already
- [ ] Output directory is clean (`rm -rf output/*`)
