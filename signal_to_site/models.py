"""Data models for Signal-to-Site pipeline."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Company(BaseModel):
    """Enriched company data from Linkt + research."""

    name: str
    domain: str
    description: Optional[str] = None
    industry: Optional[str] = None
    employee_count: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None

    # Signal-specific
    signal_type: str  # e.g., "hiring", "funding", "tech_adoption"
    signal_details: Optional[str] = None

    # Research results
    value_props: list[str] = []
    pain_points: list[str] = []
    tone: Optional[str] = None  # e.g., "professional", "casual", "technical"

    # Browser research results
    brand_colors: Optional[dict] = None  # {"primary": "#xxx", "secondary": "#xxx", "background_style": "dark/light"}
    customers: list[str] = []
    website_content: Optional[str] = None
    screenshot_path: Optional[str] = None

    # Contacts
    founders: list[dict] = []
    target_contact: Optional[dict] = None


class Signal(BaseModel):
    """A signal detected by Linkt."""

    id: str
    type: str  # "hiring", "funding", "tech_adoption"
    company_name: str
    company_domain: str
    details: str
    detected_at: datetime
    raw_data: Optional[dict] = None


class GeneratedPage(BaseModel):
    """A generated landing page."""

    company: Company
    html_content: str
    slug: str
    deployed_url: Optional[str] = None
    created_at: datetime


class OutreachDraft(BaseModel):
    """Generated outreach content."""

    company: Company
    email_subject: str
    email_body: str
    linkedin_message: Optional[str] = None
    landing_page_url: Optional[str] = None
