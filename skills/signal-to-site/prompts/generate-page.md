# Landing Page Generation Prompt

Using the brand profile for {{company_name}}, generate a personalized landing page.

## Design Requirements

The page must look like **their** team could have made it:
- Use their exact primary color ({{primary_color}}) for buttons and headers
- Use their secondary color ({{secondary_color}}) for accents
- Match their tone: {{tone}}
- Reference their actual product/company

## Content Strategy

### Hero Section
**Headline**: Connect their signal to your value prop
- If hiring: "Scaling your {{role}}? Here's how we help."
- If funding: "Congrats on the raise. Let's put it to work."
- If custom: "Built for teams like {{company_name}}"

**Subheadline**: Reference something specific from their site
- "We read about {{case_study_title}} - impressive results."
- "Your focus on {{their_differentiator}} aligns with what we do."

### Pain Points Section (3 cards)
Based on their signal, show you understand their challenges:
- Use their industry language
- Reference pain points typical for {{signal_type}} signals
- Keep it specific to their situation

### How We Help Section (3 cards)
Connect your solution to their specific context:
- Reference similar companies if possible
- Use metrics that matter to {{industry}} companies
- Match their level of technical depth

### Social Proof (optional)
If you have relevant proof:
- Similar customer in same industry
- Relevant metric or result

### CTA Section
**Headline**: Action-oriented, signal-specific
**Button**: Clear next step ("Book a Call", "See a Demo")
**Subtext**: Low commitment ("15 minutes, no pitch")

## Technical Requirements

Generate complete, valid HTML with:
- Inline CSS (no external stylesheets)
- Mobile-responsive design
- Fast loading (no external fonts, minimal images)
- Semantic HTML structure
- Meta tags for sharing

## Color Application

```css
:root {
  --primary: {{primary_color}};
  --primary-dark: /* darken primary by 10% */;
  --secondary: {{secondary_color}};
  --background: {{background_style}};
  --text: /* contrast with background */;
}
```

Use primary for:
- Buttons
- Links
- Section headers
- Accent borders

Use secondary for:
- Highlights
- Icons
- Subtle backgrounds

## Template Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{headline}} | {{your_company}}</title>
  <meta property="og:title" content="{{headline}}">
  <meta property="og:description" content="{{subheadline}}">
  <style>
    /* All CSS inline */
  </style>
</head>
<body>
  <!-- Company badge: "Built for {{company_name}}" -->

  <!-- Hero with personalized headline -->

  <!-- "We understand your challenges" section -->

  <!-- "How we help teams like yours" section -->

  <!-- CTA with {{calendly_url}} -->

  <!-- Footer -->
</body>
</html>
```

## Personalization Checklist

Before generating, verify you're including:
- [ ] Their company name (at least 3 times)
- [ ] Their exact brand colors
- [ ] A reference to something from their website
- [ ] Their signal (hiring/funding/etc) acknowledged
- [ ] Their industry language and terminology
- [ ] A specific hook that shows research

## Example Personalization

**Generic (BAD)**:
"We help companies grow faster with AI automation."

**Personalized (GOOD)**:
"We help B2B SaaS teams like {{company_name}} automate the workflows
that your new {{role}} will need to hit the ground running.
Just like you did with {{case_study_customer}}."

## Output

Generate the complete HTML file. It should be ready to deploy with no modifications needed.
