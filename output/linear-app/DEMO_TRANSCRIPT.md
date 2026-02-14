# Demo Transcript: Signal-to-Site for Linear

This is exactly what you'd see when running the demo.

---

## Input

```
You: /signal-to-site linear.app hiring Head of Sales
```

---

## Phase 1: Research (28 seconds)

```
🔍 Starting Signal-to-Site for linear.app

Signal: hiring Head of Sales

I'll now:
1. Visit their website and extract brand identity
2. Find specific hooks for personalization
3. Generate a branded landing page
4. Draft personalized outreach

Give me 60 seconds... ⏱️
```

```
📸 Visiting linear.app...
```

[Browser opens, navigates to linear.app]

```
✓ Screenshot captured
✓ Extracting brand identity...

Found:
  Company: Linear
  Tagline: "Linear is a better way to build products"
  Primary Color: #5E6AD2 (Linear purple)
  Tone: Technical, minimal, dark-mode
```

```
📄 Checking about page...
```

[Browser navigates to linear.app/about]

```
✓ Found team info

  CEO: Karri Saarinen (ex-Airbnb, ex-Coinbase)
  Stage: Series B ($52M raised)
  Employees: 50-100
```

```
🔍 Scanning for social proof...

✓ Found customers: Vercel, Ramp, Loom, Cash App, Retool
✓ Found case study: "How Ramp scaled from 50 to 500 engineers"
✓ Found stat: "10,000+ teams use Linear"
```

---

## Phase 2: Generate Assets (24 seconds)

```
🎨 Generating landing page...

  Using Linear's purple (#5E6AD2)
  Dark mode background (#0D0E12)
  Referencing: Ramp case study, Karri Saarinen

✓ Page saved to ./output/linear-app/index.html
```

```
📧 Generating outreach...

  Hook: Ramp case study (50→500 engineers)
  Target: Karri Saarinen, CEO
  Signal: Head of Sales hire

✓ Email drafted (89 words)
✓ LinkedIn message (274 chars)
✓ 3 follow-ups generated
```

---

## Phase 3: Results (52 seconds total)

```
✅ Done in 52 seconds!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 LANDING PAGE
   Location: ./output/linear-app/index.html

   Personalization:
   • Uses Linear purple (#5E6AD2)
   • Dark mode to match their brand
   • References Ramp scaling case study
   • Mentions Karri Saarinen by name
   • Headline: "Scaling your sales team at Linear?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📧 EMAIL

   To: karri@linear.app
   Subject: Re: Head of Sales role

   ─────────────────────────────────────────────────────────
   Hi Karri,

   Just saw the Head of Sales posting—congrats on the growth.
   The Ramp case study (50 to 500 engineers on Linear) is
   exactly the kind of enterprise motion that's hard to scale
   without losing the product-led magic.

   We help DevTools companies like Vercel and Supabase build
   sales processes that technical buyers actually respect.
   No sleazy tactics—just systems that convert engineering leaders.

   Put together a quick page with some thoughts specific to Linear:
   https://signal-to-site.netlify.app/linear-app

   15 minutes to compare notes?

   Best,
   Sarah
   Head of Growth, SalesBot AI
   ─────────────────────────────────────────────────────────

   Word count: 89 ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💼 LINKEDIN (274 chars)

   ─────────────────────────────────────────────────────────
   Hi Karri, loved the Ramp case study—50 to 500 engineers
   on Linear is impressive. Given you're scaling sales,
   thought I might be useful. We help DevTools companies
   build enterprise sales without losing the PLG magic.
   Would love to connect.
   ─────────────────────────────────────────────────────────

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 PERSONALIZATION HOOKS USED

   ✓ Referenced Ramp case study (50 to 500 engineers)
   ✓ Mentioned specific customer: Vercel
   ✓ Named founder: Karri Saarinen
   ✓ Matched dark/technical tone
   ✓ Signal acknowledged: Head of Sales hire

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What would you like to do?

  1. Open the landing page in browser
  2. Adjust the email copy
  3. Deploy to Netlify (get live URL)
  4. Send the email (requires approval)
```

---

## The "Wow" Moments to Point Out

1. **"See the purple? That's #5E6AD2—Linear's exact brand color."**
   - Open the generated page, show it matches linear.app

2. **"It references the Ramp case study—50 to 500 engineers."**
   - This is real content from their website
   - Only someone who researched them would know this

3. **"The email mentions Karri by name."**
   - Found on the about page
   - Personal, not generic

4. **"52 seconds total."**
   - Research + generation + personalization
   - Would take a human 30+ minutes

5. **"Dark mode, minimal design—matches their brand."**
   - Not just colors, the whole aesthetic matches

---

## Files Generated

```
output/linear-app/
├── index.html         # The landing page (open in browser)
├── outreach.json      # Email + LinkedIn + follow-ups
└── brand-profile.json # Full research data
```
