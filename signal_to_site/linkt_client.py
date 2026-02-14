"""Linkt API client for signal detection and company enrichment."""

import os
import httpx
from datetime import datetime
from typing import Optional

from .models import Signal, Company


class LinktClient:
    """Client for Linkt API - signal detection and lead intelligence."""

    BASE_URL = "https://api.linkt.ai/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("LINKT_API_KEY")
        if not self.api_key:
            raise ValueError("LINKT_API_KEY is required")

        self.client = httpx.Client(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    def get_signals(
        self,
        signal_type: Optional[str] = None,
        limit: int = 10,
    ) -> list[Signal]:
        """
        Fetch signals from Linkt.

        Args:
            signal_type: Filter by type (hiring, funding, etc.)
            limit: Max signals to return
        """
        params = {"limit": limit}
        if signal_type:
            params["type"] = signal_type

        try:
            response = self.client.get("/signal", params=params)
            response.raise_for_status()

            signals = []
            data = response.json()
            items = data.get("data", data) if isinstance(data, dict) else data

            for item in items[:limit]:
                signals.append(
                    Signal(
                        id=item.get("id", f"sig_{len(signals)}"),
                        type=item.get("type", signal_type or "unknown"),
                        company_name=item.get("company_name", item.get("name", "Unknown")),
                        company_domain=item.get("company_domain", item.get("domain", "")),
                        details=item.get("details", item.get("description", "")),
                        detected_at=datetime.fromisoformat(item["detected_at"]) if item.get("detected_at") else datetime.now(),
                        raw_data=item,
                    )
                )
            return signals

        except Exception as e:
            print(f"Error fetching signals: {e}")
            return []

    def search_entities(
        self,
        query: Optional[str] = None,
        domain: Optional[str] = None,
        limit: int = 10,
    ) -> list[dict]:
        """
        Search for companies/entities.

        Args:
            query: Search query
            domain: Filter by domain
            limit: Max results
        """
        params = {"limit": limit}
        if query:
            params["q"] = query
        if domain:
            params["domain"] = domain

        try:
            response = self.client.get("/entity/search", params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("data", data) if isinstance(data, dict) else data
        except Exception as e:
            print(f"Error searching entities: {e}")
            return []

    def get_entity(self, entity_id: str) -> Optional[dict]:
        """
        Get entity details by ID.

        Args:
            entity_id: The entity ID
        """
        try:
            response = self.client.get(f"/entity/{entity_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting entity: {e}")
            return None

    def list_entities(
        self,
        sheet_id: Optional[str] = None,
        limit: int = 10,
    ) -> list[dict]:
        """
        List entities, optionally filtered by sheet.

        Args:
            sheet_id: Filter by sheet
            limit: Max results
        """
        params = {"limit": limit}
        if sheet_id:
            params["sheet_id"] = sheet_id

        try:
            response = self.client.get("/entity", params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("data", data) if isinstance(data, dict) else data
        except Exception as e:
            print(f"Error listing entities: {e}")
            return []

    def enrich_company(self, domain: str) -> Company:
        """
        Get enriched company data.

        Args:
            domain: Company domain (e.g., "acme.com")
        """
        # Try to search for the entity by domain
        try:
            entities = self.search_entities(domain=domain, limit=1)
            if entities:
                entity = entities[0]
                return Company(
                    name=entity.get("name", domain.split(".")[0].title()),
                    domain=domain,
                    description=entity.get("description", ""),
                    industry=entity.get("industry", ""),
                    employee_count=entity.get("employee_count", ""),
                    location=entity.get("location", ""),
                    linkedin_url=entity.get("linkedin_url", ""),
                    signal_type="enrichment",
                    founders=entity.get("founders", []),
                )
        except Exception as e:
            print(f"Error enriching company: {e}")

        # Fallback to basic company info
        return Company(
            name=domain.split(".")[0].replace("-", " ").title(),
            domain=domain,
            description="",
            industry="Technology",
            signal_type="manual",
        )

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# Demo mode for testing without API key
class MockLinktClient:
    """Mock client for demo/testing purposes."""

    def get_signals(self, signal_type: Optional[str] = None, limit: int = 10, **kwargs) -> list[Signal]:
        """Return mock signals for demo."""
        all_signals = [
            Signal(
                id="sig_demo_001",
                type="hiring",
                company_name="TechStartup Inc",
                company_domain="techstartup.io",
                details="Posted job: Head of Marketing",
                detected_at=datetime.now(),
                raw_data={
                    "job_title": "Head of Marketing",
                    "job_url": "https://techstartup.io/careers/head-of-marketing",
                },
            ),
            Signal(
                id="sig_demo_002",
                type="hiring",
                company_name="CloudScale AI",
                company_domain="cloudscale.ai",
                details="Posted job: First Sales Hire - Account Executive",
                detected_at=datetime.now(),
                raw_data={
                    "job_title": "Account Executive",
                    "job_url": "https://cloudscale.ai/jobs/ae",
                },
            ),
            Signal(
                id="sig_demo_003",
                type="funding",
                company_name="DataFlow Labs",
                company_domain="dataflowlabs.com",
                details="Raised $5M Series A led by Sequoia",
                detected_at=datetime.now(),
                raw_data={
                    "amount": 5000000,
                    "round": "Series A",
                    "lead_investor": "Sequoia",
                },
            ),
        ]

        if signal_type:
            return [s for s in all_signals if s.type == signal_type][:limit]
        return all_signals[:limit]

    def search_entities(self, **kwargs) -> list[dict]:
        """Return mock search results."""
        return []

    def list_entities(self, **kwargs) -> list[dict]:
        """Return mock entity list."""
        return []

    def enrich_company(self, domain: str) -> Company:
        """Return mock enrichment data."""
        mock_data = {
            "techstartup.io": Company(
                name="TechStartup Inc",
                domain="techstartup.io",
                description="AI-powered workflow automation for SMBs",
                industry="B2B SaaS",
                employee_count="20-50",
                location="Austin, TX",
                linkedin_url="https://linkedin.com/company/techstartup",
                signal_type="hiring",
                signal_details="Hiring Head of Marketing",
                founders=[
                    {"name": "Jane Smith", "title": "CEO", "linkedin": "https://linkedin.com/in/janesmith"},
                    {"name": "John Doe", "title": "CTO", "linkedin": "https://linkedin.com/in/johndoe"},
                ],
            ),
            "cloudscale.ai": Company(
                name="CloudScale AI",
                domain="cloudscale.ai",
                description="Infrastructure optimization using machine learning",
                industry="DevOps / Infrastructure",
                employee_count="10-20",
                location="San Francisco, CA",
                linkedin_url="https://linkedin.com/company/cloudscale-ai",
                signal_type="hiring",
                signal_details="First Sales Hire",
                founders=[
                    {"name": "Alex Chen", "title": "CEO & Founder", "linkedin": "https://linkedin.com/in/alexchen"},
                ],
            ),
            "stripe.com": Company(
                name="Stripe",
                domain="stripe.com",
                description="Financial infrastructure for the internet",
                industry="FinTech / Payments",
                employee_count="5000+",
                location="San Francisco, CA",
                linkedin_url="https://linkedin.com/company/stripe",
                signal_type="hiring",
                signal_details="Head of Sales",
                founders=[
                    {"name": "Patrick Collison", "title": "CEO", "linkedin": "https://linkedin.com/in/patrickcollison"},
                    {"name": "John Collison", "title": "President", "linkedin": "https://linkedin.com/in/johncollison"},
                ],
            ),
            "linear.app": Company(
                name="Linear",
                domain="linear.app",
                description="Linear is a better way to build products. Streamline issues, sprints, and product roadmaps.",
                industry="B2B SaaS / Developer Tools",
                employee_count="50-100",
                location="San Francisco, CA",
                linkedin_url="https://linkedin.com/company/linear",
                signal_type="hiring",
                signal_details="Head of Sales",
                founders=[
                    {"name": "Karri Saarinen", "title": "CEO", "linkedin": "https://linkedin.com/in/karrisaarinen"},
                ],
            ),
        }

        if domain in mock_data:
            return mock_data[domain]

        # For unknown domains, create basic profile
        company_name = domain.split(".")[0].replace("-", " ").title()
        return Company(
            name=company_name,
            domain=domain,
            description=f"{company_name} - Technology company",
            industry="Technology",
            signal_type="custom",
        )


def get_linkt_client(demo_mode: bool = False) -> LinktClient | MockLinktClient:
    """Get Linkt client (real or mock for demo)."""
    if demo_mode or not os.getenv("LINKT_API_KEY"):
        return MockLinktClient()
    return LinktClient()
