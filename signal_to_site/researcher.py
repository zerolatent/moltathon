"""Company research module - enriches company data with AI analysis."""

import os
import httpx
from openai import OpenAI
from typing import Optional

from .models import Company


class CompanyResearcher:
    """Researches companies to extract value props, pain points, and tone."""

    def __init__(self, openai_api_key: Optional[str] = None, base_url: Optional[str] = None, use_browser: bool = True):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.use_browser = use_browser

        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")

        # Support custom endpoints (OpenAI-compatible)
        client_kwargs = {"api_key": self.openai_api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url

        self.client = OpenAI(**client_kwargs)

    def research_company(self, company: Company) -> Company:
        """
        Enrich company with research insights.

        Uses headless browser to visit site, extract brand info, then
        AI to analyze and identify value propositions, pain points, and tone.
        """
        # First, do browser research if enabled
        if self.use_browser:
            company = self._browser_research(company)

        prompt = self._build_research_prompt(company)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a sales research analyst. Analyze companies and identify "
                            "their value propositions, likely pain points, and communication style. "
                            "Be concise and actionable. You MUST output valid JSON only, no other text."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )

            result = response.choices[0].message.content
            import json
            import re

            # Try to extract JSON from response (in case there's extra text)
            json_match = re.search(r'\{[\s\S]*\}', result)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(result)
        except Exception as e:
            print(f"Error in LLM research: {e}")
            # Fallback to defaults
            data = {
                "value_props": ["Innovative solutions", "Industry expertise", "Customer focus"],
                "pain_points": ["Scaling challenges", "Market competition", "Resource optimization"],
                "tone": "professional"
            }

        # Update company with research
        company.value_props = data.get("value_props", [])
        company.pain_points = data.get("pain_points", [])
        company.tone = data.get("tone", "professional")

        return company

    def _browser_research(self, company: Company) -> Company:
        """Use headless browser to research company website."""
        try:
            from .browser import research_with_browser

            print(f"  [Browser] Visiting {company.domain}...")
            result = research_with_browser(company.domain)

            # Update company with browser research
            if result.tagline and not company.description:
                company.description = result.tagline
            if result.description:
                company.description = result.description[:500]

            # Store brand info for page generation
            company.brand_colors = {
                "primary": result.primary_color,
                "secondary": result.secondary_color,
                "background_style": result.background_style,
            }

            if result.customers:
                company.customers = result.customers

            if result.team_members:
                company.founders = result.team_members

            if result.screenshot_path:
                company.screenshot_path = result.screenshot_path

            # Add website content for LLM analysis
            company.website_content = result.text_content[:3000]

            print(f"  [Browser] Extracted brand colors: {result.primary_color}")

        except ImportError:
            print("  [Browser] Playwright not installed, skipping browser research")
        except Exception as e:
            print(f"  [Browser] Error: {e}")

        return company

    def _build_research_prompt(self, company: Company) -> str:
        """Build the research prompt for AI analysis."""
        signal_context = ""
        if company.signal_type == "hiring":
            signal_context = f"""
Signal: They are hiring for {company.signal_details or 'a key role'}.
This suggests they are scaling this function and may have pain points around:
- Building out this team/capability
- Needing tools and processes for this function
- Potential budget allocation for new solutions
"""
        elif company.signal_type == "funding":
            signal_context = f"""
Signal: They recently raised funding ({company.signal_details or 'unknown amount'}).
This suggests they are:
- Looking to scale quickly
- Have budget for new tools/solutions
- Potentially evaluating vendors
"""

        # Include website content if available
        website_section = ""
        if hasattr(company, 'website_content') and company.website_content:
            website_section = f"""
Website Content (extracted from their homepage):
{company.website_content[:2000]}
"""

        customers_section = ""
        if hasattr(company, 'customers') and company.customers:
            customers_section = f"Notable Customers: {', '.join(company.customers[:5])}"

        return f"""
Analyze this company and provide research insights.

Company: {company.name}
Domain: {company.domain}
Description: {company.description or 'Not available'}
Industry: {company.industry or 'Unknown'}
Size: {company.employee_count or 'Unknown'}
Location: {company.location or 'Unknown'}
{customers_section}

{signal_context}
{website_section}

Return JSON with:
{{
    "value_props": ["list of 2-3 key value propositions they likely care about"],
    "pain_points": ["list of 2-3 likely pain points based on signal and company profile"],
    "tone": "one of: professional, casual, technical, enterprise"
}}
"""

    def scrape_website(self, domain: str) -> Optional[str]:
        """
        Scrape basic info from company website.
        Returns extracted text content.
        """
        try:
            response = httpx.get(
                f"https://{domain}",
                follow_redirects=True,
                timeout=10.0,
                headers={"User-Agent": "Mozilla/5.0 (compatible; SignalToSite/1.0)"},
            )
            response.raise_for_status()

            # Basic HTML text extraction (could use BeautifulSoup for better parsing)
            from html.parser import HTMLParser

            class TextExtractor(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.text = []
                    self.skip_tags = {"script", "style", "nav", "footer", "header"}
                    self.current_tag = None

                def handle_starttag(self, tag, attrs):
                    self.current_tag = tag

                def handle_data(self, data):
                    if self.current_tag not in self.skip_tags:
                        text = data.strip()
                        if text:
                            self.text.append(text)

            parser = TextExtractor()
            parser.feed(response.text)
            return " ".join(parser.text)[:5000]  # Limit to 5000 chars

        except Exception as e:
            print(f"Failed to scrape {domain}: {e}")
            return None


class MockCompanyResearcher:
    """Mock researcher for demo/testing."""

    def research_company(self, company: Company) -> Company:
        """Return mock research data."""
        mock_research = {
            "techstartup.io": {
                "value_props": [
                    "Reduce manual workflow time by 80%",
                    "Easy integration with existing tools",
                    "AI-powered automation that learns from usage",
                ],
                "pain_points": [
                    "Building marketing team from scratch",
                    "Need marketing automation and analytics",
                    "Scaling customer acquisition efficiently",
                ],
                "tone": "professional",
            },
            "cloudscale.ai": {
                "value_props": [
                    "Cut cloud costs by 40% with ML optimization",
                    "Auto-scaling that actually works",
                    "DevOps team productivity boost",
                ],
                "pain_points": [
                    "First sales hire - building sales process",
                    "Need CRM and sales enablement tools",
                    "Scaling revenue without scaling headcount",
                ],
                "tone": "technical",
            },
        }

        data = mock_research.get(
            company.domain,
            {
                "value_props": ["Increase efficiency", "Save time", "Reduce costs"],
                "pain_points": ["Scaling challenges", "Process automation", "Team productivity"],
                "tone": "professional",
            },
        )

        company.value_props = data["value_props"]
        company.pain_points = data["pain_points"]
        company.tone = data["tone"]
        return company

    def scrape_website(self, domain: str) -> Optional[str]:
        return f"Mock website content for {domain}"


def get_researcher(demo_mode: bool = False) -> CompanyResearcher | MockCompanyResearcher:
    """Get researcher (real or mock for demo)."""
    if demo_mode or not os.getenv("OPENAI_API_KEY"):
        return MockCompanyResearcher()
    return CompanyResearcher()
