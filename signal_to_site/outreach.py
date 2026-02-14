"""Outreach module - generates and sends personalized outreach."""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from openai import OpenAI

from .models import Company, OutreachDraft


class OutreachGenerator:
    """Generates personalized outreach emails and messages."""

    def __init__(
        self,
        sender_name: str,
        sender_title: str,
        your_company_name: str,
        openai_api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.sender_name = sender_name
        self.sender_title = sender_title
        self.your_company_name = your_company_name

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

    def generate_outreach(
        self,
        company: Company,
        landing_page_url: Optional[str] = None,
    ) -> OutreachDraft:
        """
        Generate personalized outreach content.

        Args:
            company: Target company with research data
            landing_page_url: URL to the personalized landing page
        """
        if self.client:
            return self._generate_outreach_ai(company, landing_page_url)
        return self._generate_outreach_template(company, landing_page_url)

    def _generate_outreach_ai(
        self,
        company: Company,
        landing_page_url: Optional[str],
    ) -> OutreachDraft:
        """Generate outreach using AI."""
        # Find target contact
        target = company.target_contact or (company.founders[0] if company.founders else None)
        target_name = target.get("name", "there") if target else "there"
        target_title = target.get("title", "") if target else ""

        prompt = f"""
Generate personalized B2B sales outreach for cold email.

Target Company: {company.name}
Target Person: {target_name} ({target_title})
Industry: {company.industry or 'Technology'}
Company Size: {company.employee_count or 'Unknown'}

Signal: {company.signal_type} - {company.signal_details or 'N/A'}

Their pain points:
{chr(10).join(f'- {p}' for p in company.pain_points)}

Our company: {self.your_company_name}
Sender: {self.sender_name}, {self.sender_title}

Landing page URL: {landing_page_url or '[LANDING_PAGE_URL]'}

Generate JSON with:
{{
    "email_subject": "Short, personalized subject line (no spam words)",
    "email_body": "3-4 paragraph cold email. Reference the signal naturally. Include the landing page link. End with soft CTA. Keep it under 150 words.",
    "linkedin_message": "Short LinkedIn connection request message (under 300 chars)"
}}

Tone: {company.tone or 'professional'}. Be human, not salesy.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert B2B sales copywriter. Write personalized, "
                            "human outreach that references specific signals. Never be pushy. "
                            "You MUST output valid JSON only, no other text."
                        ),
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
                data = json.loads(json_match.group())
            else:
                data = json.loads(result)

            return OutreachDraft(
                company=company,
                email_subject=data["email_subject"],
                email_body=data["email_body"],
                linkedin_message=data.get("linkedin_message"),
                landing_page_url=landing_page_url,
            )
        except Exception as e:
            print(f"Error generating outreach with AI: {e}")
            return self._generate_outreach_template(company, landing_page_url)

    def _generate_outreach_template(
        self,
        company: Company,
        landing_page_url: Optional[str],
    ) -> OutreachDraft:
        """Generate outreach using templates."""
        target = company.target_contact or (company.founders[0] if company.founders else None)
        target_name = target.get("name", "there") if target else "there"

        # Generate subject based on signal
        if company.signal_type == "hiring":
            subject = f"Re: {company.name}'s {company.signal_details or 'new hire'}"
            opening = f"Noticed you're hiring for {company.signal_details or 'a key role'} - congrats on the growth!"
        elif company.signal_type == "funding":
            subject = f"Congrats on the raise, {company.name}!"
            opening = f"Saw the news about your recent funding round - exciting times!"
        else:
            subject = f"Quick question for {company.name}"
            opening = f"I've been following {company.name}'s progress and had a quick thought."

        page_link = f"\n\nI put together a quick page with some ideas specifically for {company.name}: {landing_page_url}" if landing_page_url else ""

        email_body = f"""Hi {target_name},

{opening}

{company.pain_points[0] if company.pain_points else 'Scaling efficiently'} is something we help teams with at {self.your_company_name}. {company.value_props[0] if company.value_props else 'We help companies like yours grow faster.'}{page_link}

Would you be open to a quick 15-min chat to see if there's a fit?

Best,
{self.sender_name}
{self.sender_title}, {self.your_company_name}"""

        linkedin_message = (
            f"Hi {target_name}! Saw {company.name} is {company.signal_details or 'growing'}. "
            f"We help similar companies with {company.pain_points[0] if company.pain_points else 'scaling'}. "
            f"Would love to connect!"
        )[:300]

        return OutreachDraft(
            company=company,
            email_subject=subject,
            email_body=email_body,
            linkedin_message=linkedin_message,
            landing_page_url=landing_page_url,
        )


class EmailSender:
    """Sends emails via SMTP."""

    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        smtp_user: Optional[str] = None,
        smtp_password: Optional[str] = None,
    ):
        self.smtp_host = smtp_host or os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = smtp_port or int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = smtp_user or os.getenv("SMTP_USER")
        self.smtp_password = smtp_password or os.getenv("SMTP_PASSWORD")

        if not self.smtp_user or not self.smtp_password:
            raise ValueError("SMTP_USER and SMTP_PASSWORD are required")

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        from_name: Optional[str] = None,
    ) -> bool:
        """
        Send an email.

        Returns True if successful.
        """
        try:
            msg = MIMEMultipart()
            msg["From"] = f"{from_name} <{self.smtp_user}>" if from_name else self.smtp_user
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False


class MockEmailSender:
    """Mock sender for demo (just logs)."""

    def send_email(self, to_email: str, subject: str, body: str, **kwargs) -> bool:
        print(f"\n{'='*50}")
        print(f"[MOCK EMAIL] To: {to_email}")
        print(f"Subject: {subject}")
        print(f"{'='*50}")
        print(body)
        print(f"{'='*50}\n")
        return True


def get_email_sender(demo_mode: bool = False) -> EmailSender | MockEmailSender:
    """Get email sender (real or mock)."""
    if demo_mode or not os.getenv("SMTP_USER"):
        return MockEmailSender()
    return EmailSender()
