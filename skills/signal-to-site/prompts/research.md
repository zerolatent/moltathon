# Company Research Prompt

You are researching {{company_domain}} to create hyper-personalized sales outreach.

## Your Mission
Extract everything needed to create a landing page that looks like THEIR team made it, and an email that feels like you've been following them for months.

## Step 1: Homepage Deep Dive

Use the browser tool to:
1. Navigate to https://{{company_domain}}
2. Take a full-page screenshot
3. Extract all visible text

While analyzing, identify:
- **Primary brand color** (the dominant color in their header/buttons)
- **Secondary color** (accent color, often used for links/highlights)
- **Background style** (light/dark mode, gradients, patterns)
- **Logo** (describe it, note if text-based or icon-based)
- **Main headline/tagline** (exact text)
- **Navigation items** (what pages do they have?)
- **Hero section CTA** (what action do they want visitors to take?)

## Step 2: About Page

Navigate to /about, /company, or /team:
- **Company description** (what do they do, in their words?)
- **Founding story** (when founded, by whom, why?)
- **Team members** (names, titles, especially founders/C-suite)
- **Company size/stage** (employees, funding, customers)
- **Mission/values** (what do they believe?)

## Step 3: Product/Solution Understanding

Navigate to /product, /solutions, /features, or /how-it-works:
- **Core product** (what do they sell?)
- **Target audience** (who is it for?)
- **Key features** (top 3 capabilities)
- **Pricing model** (if visible - freemium, enterprise, usage-based?)
- **Differentiator** (what makes them unique?)

## Step 4: Social Proof Hunt

Look for /customers, /case-studies, /testimonials:
- **Customer logos** (list recognizable names)
- **Case study titles** (specific results mentioned)
- **Testimonial quotes** (pick the most compelling one)
- **Metrics** (any numbers they brag about - users, revenue, savings)

## Step 5: Recent Activity

Check /blog or /news (just the latest 2-3 items):
- **Recent blog post titles** (shows what they're thinking about)
- **News/press mentions** (recent wins, launches)
- **Content themes** (what topics do they write about?)

## Step 6: Voice & Tone Analysis

Based on all content, characterize their communication:
- **Formality**: Corporate / Professional / Casual / Playful
- **Technical depth**: Simplified / Balanced / Deep-dive
- **Personality**: Serious / Friendly / Edgy / Authoritative
- **Industry jargon**: Heavy / Light / Avoided

## Output Format

After research, compile this Brand Profile:

```json
{
  "company": {
    "name": "Exact company name",
    "domain": "{{company_domain}}",
    "tagline": "Their exact tagline",
    "description": "One sentence description",
    "industry": "e.g., B2B SaaS, DevTools, FinTech",
    "stage": "e.g., Seed, Series A, Growth",
    "employee_count": "estimate or exact"
  },
  "brand": {
    "primary_color": "#hexcode",
    "secondary_color": "#hexcode",
    "background": "light/dark",
    "font_style": "modern/traditional/playful",
    "tone": "professional/casual/technical"
  },
  "product": {
    "name": "Product name",
    "description": "What it does",
    "target_audience": "Who it's for",
    "key_benefit": "Main value prop",
    "differentiator": "What makes it unique"
  },
  "social_proof": {
    "customer_logos": ["Customer1", "Customer2"],
    "best_case_study": "Title or summary",
    "key_metric": "e.g., 10,000 users, $5M saved"
  },
  "hooks": {
    "recent_blog": "Title of most recent blog post",
    "team_member": {"name": "CEO name", "title": "CEO"},
    "specific_detail": "Something unique only a researcher would find"
  },
  "signal": {
    "type": "{{signal_type}}",
    "details": "{{signal_details}}"
  }
}
```

## Important Notes

- Be thorough but fast - we're aiming for 60 seconds total
- If a page doesn't exist, skip it and move on
- Extract EXACT text for taglines and headlines (we'll use them)
- Colors should be actual hex codes from their CSS
- The "specific_detail" hook is crucial - find something unexpected
