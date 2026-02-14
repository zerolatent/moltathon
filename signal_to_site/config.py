"""Configuration management for Signal-to-Site."""

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from dotenv import load_dotenv


class Config(BaseModel):
    """Application configuration."""

    # Your company info (required for personalization)
    your_company_name: str = "Your Company"
    your_value_prop: str = "We help companies grow faster"
    sender_name: str = "Alex"
    sender_title: str = "Founder"
    cta_url: str = "https://calendly.com/your-link"

    # API Keys
    linkt_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    # Deployment
    deploy_platform: str = "local"  # "local", "netlify"
    netlify_token: Optional[str] = None
    netlify_site_id: Optional[str] = None

    # Notifications
    notify_platform: str = "mock"  # "mock", "slack", "telegram"
    slack_webhook_url: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None

    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None

    # Pipeline settings
    max_signals: int = 10
    signal_types: list[str] = ["hiring", "funding"]

    @classmethod
    def from_env(cls, env_file: Optional[str] = None) -> "Config":
        """Load config from environment variables."""
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        return cls(
            your_company_name=os.getenv("YOUR_COMPANY_NAME", "Your Company"),
            your_value_prop=os.getenv("YOUR_VALUE_PROP", "We help companies grow faster"),
            sender_name=os.getenv("SENDER_NAME", "Alex"),
            sender_title=os.getenv("SENDER_TITLE", "Founder"),
            cta_url=os.getenv("CTA_URL", "https://calendly.com/your-link"),
            linkt_api_key=os.getenv("LINKT_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            deploy_platform=os.getenv("DEPLOY_PLATFORM", "local"),
            netlify_token=os.getenv("NETLIFY_TOKEN"),
            netlify_site_id=os.getenv("NETLIFY_SITE_ID"),
            notify_platform=os.getenv("NOTIFY_PLATFORM", "mock"),
            slack_webhook_url=os.getenv("SLACK_WEBHOOK_URL"),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
            smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_user=os.getenv("SMTP_USER"),
            smtp_password=os.getenv("SMTP_PASSWORD"),
            max_signals=int(os.getenv("MAX_SIGNALS", "10")),
        )

    @property
    def is_demo_mode(self) -> bool:
        """Check if running in demo mode (no API keys)."""
        return not self.linkt_api_key

    def validate_for_production(self) -> list[str]:
        """Check what's missing for production mode."""
        missing = []

        if not self.linkt_api_key:
            missing.append("LINKT_API_KEY")
        if not self.openai_api_key:
            missing.append("OPENAI_API_KEY (optional, enables AI content)")

        if self.deploy_platform == "netlify" and not self.netlify_token:
            missing.append("NETLIFY_TOKEN")

        if self.notify_platform == "slack" and not self.slack_webhook_url:
            missing.append("SLACK_WEBHOOK_URL")
        if self.notify_platform == "telegram" and not self.telegram_bot_token:
            missing.append("TELEGRAM_BOT_TOKEN")

        return missing
