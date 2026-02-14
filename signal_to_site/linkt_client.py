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
        icp_id: Optional[str] = None,
        signal_type: Optional[str] = None,
        limit: int = 10,
    ) -> list[Signal]:
        """
        Fetch signals matching criteria.

        Args:
            icp_id: Filter by ICP (Ideal Customer Profile) ID
            signal_type: Filter by type (hiring, funding, tech_adoption)
            limit: Max signals to return
        """
        params = {"limit": limit}
        if icp_id:
            params["icp_id"] = icp_id
        if signal_type:
            params["type"] = signal_type

        response = self.client.get("/signals", params=params)
        response.raise_for_status()

        signals = []
        for item in response.json().get("data", []):
            signals.append(
                Signal(
                    id=item["id"],
                    type=item["type"],
                    company_name=item["company"]["name"],
                    company_domain=item["company"]["domain"],
                    details=item.get("details", ""),
                    detected_at=datetime.fromisoformat(item["detected_at"]),
                    raw_data=item,
                )
            )
        return signals

    def search_companies(
        self,
        query: str,
        location: Optional[str] = None,
        employee_min: Optional[int] = None,
        employee_max: Optional[int] = None,
        signal_type: Optional[str] = None,
        limit: int = 10,
    ) -> list[dict]:
        """
        Search for companies matching criteria.

        Args:
            query: Search query (industry, keywords, etc.)
            location: Filter by location
            employee_min: Minimum employee count
            employee_max: Maximum employee count
            signal_type: Companies with this signal type
            limit: Max results
        """
        payload = {
            "query": query,
            "limit": limit,
        }
        if location:
            payload["location"] = location
        if employee_min:
            payload["employee_min"] = employee_min
        if employee_max:
            payload["employee_max"] = employee_max
        if signal_type:
            payload["signal_type"] = signal_type

        response = self.client.post("/search", json=payload)
        response.raise_for_status()
        return response.json().get("data", [])

    def enrich_company(self, domain: str) -> Company:
        """
        Get enriched company data.

        Args:
            domain: Company domain (e.g., "acme.com")
        """
        response = self.client.get(f"/companies/{domain}")
        response.raise_for_status()

        data = response.json()
        return Company(
            name=data.get("name", domain),
            domain=domain,
            description=data.get("description"),
            industry=data.get("industry"),
            employee_count=data.get("employee_count"),
            location=data.get("location"),
            linkedin_url=data.get("linkedin_url"),
            signal_type="enrichment",
            founders=data.get("founders", []),
        )

    def create_icp(
        self,
        name: str,
        criteria: dict,
    ) -> dict:
        """
        Create an Ideal Customer Profile for signal monitoring.

        Args:
            name: ICP name
            criteria: Filter criteria (location, industry, employee_range, etc.)
        """
        payload = {
            "name": name,
            "criteria": criteria,
        }
        response = self.client.post("/icps", json=payload)
        response.raise_for_status()
        return response.json()

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

    def get_signals(self, **kwargs) -> list[Signal]:
        """Return mock signals for demo."""
        return [
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
        }
        return mock_data.get(
            domain,
            Company(
                name=domain.split(".")[0].title(),
                domain=domain,
                description="Technology company",
                industry="Technology",
                signal_type="unknown",
            ),
        )


def get_linkt_client(demo_mode: bool = False) -> LinktClient | MockLinktClient:
    """Get Linkt client (real or mock for demo)."""
    if demo_mode or not os.getenv("LINKT_API_KEY"):
        return MockLinktClient()
    return LinktClient()
