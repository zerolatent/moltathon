# Outreach Generation Prompt

Using the brand profile for {{company_name}}, generate personalized outreach.

## The Golden Rule

Every piece of outreach must contain something that **only someone who researched them would know**.

NOT: "I see you're growing..."
YES: "I just read your case study about {{customer}} saving {{metric}} - impressive results."

NOT: "Your company seems interesting..."
YES: "{{founder_name}}, the way you described {{specific_thing}} on your about page resonated with me."

## Email Draft

### Subject Line Rules
- Under 50 characters
- Reference something specific
- No spam words (free, guaranteed, limited time)
- Create curiosity

**Signal-Based Subject Templates**:
- Hiring: "Re: Your {{role}} search"
- Hiring: "Saw the {{role}} post - quick thought"
- Hiring: "For your new {{role}}"
- Funding: "Congrats from a fellow {{industry}} builder"
- Funding: "Post-raise scaling thought"
- Custom: "{{Specific thing from their site}}"

### Email Body Structure

**Opening (1 sentence)**:
Hook them with specificity. Reference:
- Their recent blog post
- Their case study
- A specific product feature
- Their founding story
- Recent news about them

Example: "Just read your piece on {{blog_topic}} - the part about {{specific_insight}} was spot on."

**Bridge (1-2 sentences)**:
Connect your observation to their current situation (the signal):
- "Given you're now hiring for {{role}}, I imagine {{pain_point}} is top of mind."
- "Post-raise, most teams in {{industry}} prioritize {{common_priority}}."

**Value (1-2 sentences)**:
Briefly introduce how you help, connected to their context:
- "We help {{similar_companies}} with exactly this - {{your_value_prop}}."
- "{{Your_company}} does {{what_you_do}}, which {{specific_benefit}} for teams like yours."

**Proof (1 sentence, optional)**:
If relevant, one piece of social proof:
- "{{Similar_customer}} saw {{result}} in {{timeframe}}."

**CTA (1 sentence)**:
Low-commitment ask:
- "Would you be open to a 15-min call to see if there's a fit?"
- "Happy to share how we approached this with {{similar_company}} - interested?"
- "Built a quick page showing how this could work for {{company_name}}: {{page_url}}"

**Sign-off**:
Brief and personal:
- "Best, {{sender_name}}"
- Include title only if it adds credibility

### Email Constraints
- Total length: Under 150 words
- Paragraphs: Max 2 sentences each
- No bullet points or formatting
- Reads like a human wrote it quickly
- Match their tone ({{tone}})

## LinkedIn Connection Request

**Character limit**: 300 characters

**Formula**: Specific observation + relevance + soft ask

**Template**:
"Hi {{first_name}}, [specific thing from research]. [Connection to signal/relevance]. Would love to connect and share thoughts."

**Examples**:
- "Hi Sarah, loved the Acme case study - 40 hrs/week saved is no joke. Given you're scaling marketing, thought I might be able to help. Would love to connect."
- "Hi Alex, your post on infrastructure optimization was spot on. We work with similar DevOps teams. Would be great to connect."

## Follow-Up Sequence (3 touches)

### Follow-Up 1 (Day 3)
Short, add value:
- Share a relevant article/resource
- Reference something new from their company
- "Bumping this" is lazy - add something

### Follow-Up 2 (Day 7)
Different angle:
- Different benefit of your solution
- Different social proof
- Ask a question instead of making an ask

### Follow-Up 3 (Day 14)
Break-up email:
- Acknowledge they're busy
- Leave the door open
- "No worries if timing isn't right - happy to reconnect when {{role}} is settled."

## Output Format

```json
{
  "email": {
    "subject": "Subject line here",
    "body": "Full email body here",
    "to": "{{target_email if known}}",
    "follow_ups": [
      {"day": 3, "subject": "...", "body": "..."},
      {"day": 7, "subject": "...", "body": "..."},
      {"day": 14, "subject": "...", "body": "..."}
    ]
  },
  "linkedin": {
    "connection_request": "300 char message",
    "inmail_if_needed": "Longer version if not connected"
  },
  "personalization_hooks_used": [
    "Referenced case study: {{case_study}}",
    "Mentioned team member: {{founder}}",
    "Used their tagline: {{tagline}}"
  ]
}
```

## Quality Checklist

Before finalizing, verify:
- [ ] Subject line is specific and under 50 chars
- [ ] Opening references something specific from their site
- [ ] Signal (hiring/funding) is acknowledged naturally
- [ ] Total word count under 150
- [ ] CTA is low-commitment
- [ ] LinkedIn message under 300 chars
- [ ] Tone matches their brand voice ({{tone}})
- [ ] At least 2 personalization hooks used
- [ ] No generic phrases ("hope this finds you well", "I'd love to connect")
