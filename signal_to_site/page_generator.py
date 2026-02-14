"""Landing page generator - creates personalized pages from templates."""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader
from openai import OpenAI

from .models import Company, GeneratedPage


class PageGenerator:
    """Generates personalized landing pages for target companies."""

    def __init__(
        self,
        your_company_name: str,
        your_value_prop: str,
        cta_url: str = "https://calendly.com/your-link",
        openai_api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.your_company_name = your_company_name
        self.your_value_prop = your_value_prop
        self.cta_url = cta_url

        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        if self.openai_api_key:
            client_kwargs = {"api_key": self.openai_api_key}
            if self.base_url:
                client_kwargs["base_url"] = self.base_url
            self.client = OpenAI(**client_kwargs)
        else:
            self.client = None

        # Set up Jinja2 templates
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate_page(self, company: Company) -> GeneratedPage:
        """
        Generate a personalized landing page for a company.

        Args:
            company: Enriched company data with research insights
        """
        # Generate personalized copy
        copy = self._generate_copy(company)

        # Extract brand colors from browser research
        brand_colors = company.brand_colors or {}
        primary_color = brand_colors.get("primary", "#2563eb")
        secondary_color = brand_colors.get("secondary", "#1e293b")
        background_style = brand_colors.get("background_style", "light")

        # Render HTML template
        template = self.env.get_template("landing_page.html")
        html = template.render(
            company_name=company.name,
            headline=copy["headline"],
            subheadline=copy["subheadline"],
            pain_points=copy["pain_points"],
            value_props=copy["value_props"],
            cta_text=copy["cta_text"],
            cta_action=copy["cta_action"],
            cta_url=self.cta_url,
            your_company_name=self.your_company_name,
            year=datetime.now().year,
            # Brand colors from browser research
            primary_color=primary_color,
            secondary_color=secondary_color,
            background_style=background_style,
            customers=company.customers[:3] if company.customers else [],
        )

        # Generate URL-safe slug
        slug = self._generate_slug(company.name)

        return GeneratedPage(
            company=company,
            html_content=html,
            slug=slug,
            created_at=datetime.now(),
        )

    def _generate_copy(self, company: Company) -> dict:
        """Generate personalized marketing copy using AI."""
        if self.client:
            return self._generate_copy_ai(company)
        return self._generate_copy_template(company)

    def _generate_copy_ai(self, company: Company) -> dict:
        """Generate copy using OpenAI."""
        prompt = f"""
Generate personalized landing page copy for a B2B outreach page.

Target company: {company.name}
Industry: {company.industry or 'Technology'}
Signal: {company.signal_type} - {company.signal_details or 'N/A'}

Their likely pain points:
{chr(10).join(f'- {p}' for p in company.pain_points)}

Our value proposition: {self.your_value_prop}

Generate JSON with:
{{
    "headline": "Compelling headline mentioning their company or situation (under 10 words)",
    "subheadline": "1-2 sentence value prop specific to their situation",
    "pain_points": [
        {{"title": "Pain point title", "description": "Why this matters to them"}},
        {{"title": "Pain point title", "description": "Why this matters to them"}},
        {{"title": "Pain point title", "description": "Why this matters to them"}}
    ],
    "value_props": [
        {{"title": "How we help", "description": "Specific benefit"}},
        {{"title": "How we help", "description": "Specific benefit"}},
        {{"title": "How we help", "description": "Specific benefit"}}
    ],
    "cta_text": "Button text (e.g., 'Schedule a Demo')",
    "cta_action": "verb phrase (e.g., 'transform your workflow')"
}}

Keep it {company.tone or 'professional'} in tone. Be specific to their situation.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a conversion copywriter. Write compelling, specific landing page copy. You MUST output valid JSON only, no other text.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.8,
            )

            import json
            import re
            result = response.choices[0].message.content
            json_match = re.search(r'\{[\s\S]*\}', result)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(result)
        except Exception as e:
            print(f"Error generating copy with AI: {e}")
            return self._generate_copy_template(company)

    def _generate_copy_template(self, company: Company) -> dict:
        """Generate copy using templates (no AI required)."""
        # Map signal type to messaging
        if company.signal_type == "hiring":
            headline = f"Scaling your {company.signal_details or 'team'}?"
            subheadline = (
                f"We help companies like {company.name} build and scale faster with "
                f"{self.your_value_prop}."
            )
            cta_action = "accelerate your growth"
        elif company.signal_type == "funding":
            headline = f"Congratulations on the raise, {company.name}!"
            subheadline = (
                f"Smart companies use their runway wisely. {self.your_value_prop} "
                "helps you scale efficiently."
            )
            cta_action = "maximize your runway"
        else:
            headline = f"Built for teams like {company.name}"
            subheadline = f"See how {self.your_value_prop} can help your team."
            cta_action = "see how we can help"

        # Convert pain points to structured format
        pain_points = []
        for i, pain in enumerate(company.pain_points[:3]):
            pain_points.append({
                "title": pain if len(pain) < 50 else pain[:47] + "...",
                "description": f"We've seen this challenge at companies your size. Here's how we help.",
            })

        # Ensure we have 3 pain points
        while len(pain_points) < 3:
            pain_points.append({
                "title": "Scaling efficiently",
                "description": "Growth brings complexity. We help you manage it.",
            })

        # Convert value props to structured format
        value_props = []
        for i, value in enumerate(company.value_props[:3]):
            value_props.append({
                "title": value if len(value) < 50 else value[:47] + "...",
                "description": "Proven results with teams like yours.",
            })

        # Ensure we have 3 value props
        while len(value_props) < 3:
            value_props.append({
                "title": "Proven results",
                "description": "See measurable impact from day one.",
            })

        return {
            "headline": headline,
            "subheadline": subheadline,
            "pain_points": pain_points,
            "value_props": value_props,
            "cta_text": "Book a Demo",
            "cta_action": cta_action,
        }

    def _generate_slug(self, company_name: str) -> str:
        """Generate URL-safe slug from company name."""
        # Remove special characters, lowercase, replace spaces with dashes
        slug = company_name.lower()
        slug = re.sub(r"[^a-z0-9\s-]", "", slug)
        slug = re.sub(r"[\s_]+", "-", slug)
        slug = re.sub(r"-+", "-", slug)
        return slug.strip("-")

    def save_page(self, page: GeneratedPage, output_dir: str = "./output") -> str:
        """Save generated page to local filesystem."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        page_file = output_path / f"{page.slug}.html"
        page_file.write_text(page.html_content)

        return str(page_file)
