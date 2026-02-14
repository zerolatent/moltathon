"""Main pipeline orchestrator - ties everything together."""

import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .models import Company, Signal, GeneratedPage, OutreachDraft
from .linkt_client import get_linkt_client
from .researcher import get_researcher
from .page_generator import PageGenerator
from .deployer import get_deployer
from .outreach import OutreachGenerator, get_email_sender
from .notifications import get_notifier


@dataclass
class PipelineConfig:
    """Configuration for the pipeline."""

    # Your company info
    your_company_name: str
    your_value_prop: str
    sender_name: str
    sender_title: str
    cta_url: str = "https://calendly.com/your-link"

    # Modes
    demo_mode: bool = False
    deploy_platform: str = "local"  # "local", "netlify"
    notify_platform: str = "mock"  # "mock", "slack", "telegram"
    quiet_mode: bool = False  # Suppress console output (for JSON mode)

    # Filtering
    signal_types: list[str] | None = None  # e.g., ["hiring", "funding"]
    max_signals: int = 10


@dataclass
class PipelineResult:
    """Result of a single pipeline run for one company."""

    company: Company
    page: GeneratedPage
    outreach: OutreachDraft
    page_url: Optional[str] = None
    email_sent: bool = False
    notified: bool = False


class SignalToSitePipeline:
    """
    Main pipeline: Signal -> Research -> Page -> Deploy -> Outreach -> Notify

    This is the core orchestrator that ties together:
    1. Linkt signal detection
    2. Company research and enrichment
    3. Landing page generation
    4. Page deployment
    5. Outreach generation
    6. Notifications
    """

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.console = Console(quiet=config.quiet_mode)

        # Initialize components
        self.linkt = get_linkt_client(demo_mode=config.demo_mode)
        self.researcher = get_researcher(demo_mode=config.demo_mode)
        self.page_generator = PageGenerator(
            your_company_name=config.your_company_name,
            your_value_prop=config.your_value_prop,
            cta_url=config.cta_url,
        )
        self.deployer = get_deployer(platform=config.deploy_platform)
        self.outreach_generator = OutreachGenerator(
            sender_name=config.sender_name,
            sender_title=config.sender_title,
            your_company_name=config.your_company_name,
        )
        self.email_sender = get_email_sender(demo_mode=config.demo_mode)
        # Use "none" notifier in quiet mode to suppress output
        notify_platform = "none" if config.quiet_mode else config.notify_platform
        self.notifier = get_notifier(platform=notify_platform)

    def run(
        self,
        signal_type: Optional[str] = None,
        send_emails: bool = False,
    ) -> list[PipelineResult]:
        """
        Run the full pipeline.

        Args:
            signal_type: Filter signals by type (hiring, funding, etc.)
            send_emails: Actually send outreach emails

        Returns:
            List of results for each processed signal
        """
        results = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            # Step 1: Fetch signals
            task = progress.add_task("Fetching signals from Linkt...", total=None)
            signals = self.linkt.get_signals(
                signal_type=signal_type or (self.config.signal_types[0] if self.config.signal_types else None),
                limit=self.config.max_signals,
            )
            progress.update(task, description=f"Found {len(signals)} signals")

            if not signals:
                self.console.print("[yellow]No signals found matching criteria[/yellow]")
                return results

            # Process each signal
            for signal in signals:
                result = self._process_signal(signal, send_emails, progress)
                if result:
                    results.append(result)

        # Print summary
        self._print_summary(results)
        return results

    def _process_signal(
        self,
        signal: Signal,
        send_emails: bool,
        progress: Progress,
    ) -> Optional[PipelineResult]:
        """Process a single signal through the full pipeline."""
        try:
            # Step 2: Enrich company data
            task = progress.add_task(f"Researching {signal.company_name}...", total=None)
            company = self.linkt.enrich_company(signal.company_domain)
            company.signal_type = signal.type
            company.signal_details = signal.details

            # Step 3: Research company
            progress.update(task, description=f"Analyzing {signal.company_name}...")
            company = self.researcher.research_company(company)

            # Step 4: Generate landing page
            progress.update(task, description=f"Generating page for {signal.company_name}...")
            page = self.page_generator.generate_page(company)

            # Step 5: Deploy page
            progress.update(task, description=f"Deploying {signal.company_name} page...")
            page_url = self.deployer.deploy_page(page)
            page.deployed_url = page_url

            # Step 6: Generate outreach
            progress.update(task, description=f"Creating outreach for {signal.company_name}...")
            outreach = self.outreach_generator.generate_outreach(company, page_url)

            # Step 7: Send email (if enabled)
            email_sent = False
            if send_emails and company.target_contact:
                email = company.target_contact.get("email")
                if email:
                    email_sent = self.email_sender.send_email(
                        to_email=email,
                        subject=outreach.email_subject,
                        body=outreach.email_body,
                        from_name=self.config.sender_name,
                    )

            # Step 8: Send notification
            notified = self.notifier.send_pipeline_result(company, page, outreach)

            progress.update(task, description=f"[green]Done: {signal.company_name}[/green]")

            return PipelineResult(
                company=company,
                page=page,
                outreach=outreach,
                page_url=page_url,
                email_sent=email_sent,
                notified=notified,
            )

        except Exception as e:
            import traceback
            self.console.print(f"[red]Error processing {signal.company_name}: {e}[/red]")
            self.console.print(f"[dim]{traceback.format_exc()}[/dim]")
            return None

    def _print_summary(self, results: list[PipelineResult]):
        """Print a summary table of results."""
        if not results:
            return

        self.console.print("\n")

        table = Table(title="Pipeline Results")
        table.add_column("Company", style="cyan")
        table.add_column("Signal", style="magenta")
        table.add_column("Page URL", style="green")
        table.add_column("Email Subject", style="yellow")

        for r in results:
            table.add_row(
                r.company.name,
                f"{r.company.signal_type}: {r.company.signal_details or 'N/A'}"[:40],
                r.page_url[:50] if r.page_url else "N/A",
                r.outreach.email_subject[:40],
            )

        self.console.print(table)
        self.console.print(f"\n[bold]Processed {len(results)} signals successfully![/bold]\n")

    def run_single(
        self,
        domain: str,
        signal_type: str = "custom",
        signal_details: str = "",
        send_email: bool = False,
    ) -> Optional[PipelineResult]:
        """
        Run pipeline for a single company by domain.

        Useful for testing or manual triggers.
        """
        self.console.print(f"\n[bold]Processing {domain}...[/bold]\n")

        # Create a mock signal
        signal = Signal(
            id=f"manual_{domain}",
            type=signal_type,
            company_name=domain.split(".")[0].title(),
            company_domain=domain,
            details=signal_details,
            detected_at=datetime.now(),
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            return self._process_signal(signal, send_email, progress)
