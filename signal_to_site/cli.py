"""CLI for Signal-to-Site pipeline.

Supports both human-readable output and JSON output for OpenClaw/Lobster integration.
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from .pipeline import SignalToSitePipeline, PipelineConfig, PipelineResult


def main():
    """Main CLI entrypoint."""
    # Load environment variables
    load_dotenv()

    args = sys.argv[1:]
    json_mode = "--json" in args

    # Create console (quiet in JSON mode)
    console = Console(quiet=json_mode)

    # Handle subcommands for OpenClaw integration
    if args and args[0] in ["fetch", "research", "generate-pages", "deploy", "draft-outreach", "send", "notify"]:
        return _handle_subcommand(args[0], args[1:], json_mode)

    # Print banner (only in human mode)
    if not json_mode:
        console.print(
            Panel.fit(
                "[bold blue]Signal-to-Site[/bold blue]\n"
                "[dim]GTM Signal-to-Outreach Pipeline[/dim]",
                border_style="blue",
            )
        )

    if "--help" in args or "-h" in args:
        _print_help(console)
        return

    # Determine mode
    demo_mode = "--demo" in args or not os.getenv("LINKT_API_KEY")

    if demo_mode and not json_mode:
        console.print("\n[yellow]Running in DEMO mode (using mock data)[/yellow]")
        console.print("[dim]Set LINKT_API_KEY and OPENAI_API_KEY for production mode[/dim]\n")

    # Get config from env or defaults
    config = PipelineConfig(
        your_company_name=os.getenv("YOUR_COMPANY_NAME", "Acme Inc"),
        your_value_prop=os.getenv("YOUR_VALUE_PROP", "AI-powered automation that saves you 10+ hours/week"),
        sender_name=os.getenv("SENDER_NAME", "Alex"),
        sender_title=os.getenv("SENDER_TITLE", "Founder"),
        cta_url=os.getenv("CTA_URL", "https://calendly.com/your-link"),
        demo_mode=demo_mode,
        deploy_platform="local" if demo_mode else os.getenv("DEPLOY_PLATFORM", "local"),
        notify_platform="mock" if demo_mode else os.getenv("NOTIFY_PLATFORM", "mock"),
        quiet_mode=json_mode,
        max_signals=int(os.getenv("MAX_SIGNALS", "5")),
    )

    # Create and run pipeline
    pipeline = SignalToSitePipeline(config)

    # Check for single-company mode
    if "--domain" in args:
        domain_idx = args.index("--domain") + 1
        if domain_idx < len(args):
            domain = args[domain_idx]
            signal_type = "hiring"
            signal_details = "Custom test signal"

            if "--signal" in args:
                sig_idx = args.index("--signal") + 1
                if sig_idx < len(args):
                    signal_type = args[sig_idx]

            result = pipeline.run_single(
                domain=domain,
                signal_type=signal_type,
                signal_details=signal_details,
            )

            if result:
                if json_mode:
                    print(json.dumps(_result_to_dict(result), indent=2))
                else:
                    _print_single_result(console, result)
            return

    # Default: run full pipeline
    signal_type = None
    if "--type" in args:
        type_idx = args.index("--type") + 1
        if type_idx < len(args):
            signal_type = args[type_idx]

    # Get limit
    limit = int(os.getenv("MAX_SIGNALS", "5"))
    if "--limit" in args:
        limit_idx = args.index("--limit") + 1
        if limit_idx < len(args):
            limit = int(args[limit_idx])
            config.max_signals = limit

    send_emails = "--send-emails" in args

    results = pipeline.run(signal_type=signal_type, send_emails=send_emails)

    if json_mode:
        # Output JSON for OpenClaw/Lobster
        output = {
            "success": True,
            "count": len(results),
            "signals_processed": len(results),
            "pages_generated": len(results),
            "outreach_drafted": len(results),
            "results": [_result_to_dict(r) for r in results],
            "page_urls": [r.page_url for r in results if r.page_url],
            "summary": f"Processed {len(results)} signals, generated {len(results)} pages",
        }
        print(json.dumps(output, indent=2))
    elif results:
        console.print("\n[bold green]Pipeline complete![/bold green]")
        console.print(f"Generated {len(results)} landing pages.\n")

        if config.deploy_platform == "local":
            output_path = Path("./output").absolute()
            console.print(f"[dim]Pages saved to: {output_path}[/dim]")
            console.print(f"[dim]Open: file://{output_path}/index.html[/dim]\n")


def _handle_subcommand(command: str, args: list, json_mode: bool):
    """Handle subcommands for Lobster workflow integration."""
    import sys

    # Read stdin if available (for piping)
    stdin_data = None
    if "--stdin" in args and not sys.stdin.isatty():
        stdin_data = json.load(sys.stdin)

    demo_mode = "--demo" in args or not os.getenv("LINKT_API_KEY")

    if command == "fetch":
        # Fetch signals from Linkt
        from .linkt_client import get_linkt_client

        signal_type = "hiring"
        limit = 5
        if "--type" in args:
            idx = args.index("--type") + 1
            if idx < len(args):
                signal_type = args[idx]
        if "--limit" in args:
            idx = args.index("--limit") + 1
            if idx < len(args):
                limit = int(args[idx])

        client = get_linkt_client(demo_mode=demo_mode)
        signals = client.get_signals(signal_type=signal_type, limit=limit)

        output = {
            "signals": [
                {
                    "id": s.id,
                    "type": s.type,
                    "company_name": s.company_name,
                    "company_domain": s.company_domain,
                    "details": s.details,
                    "detected_at": s.detected_at.isoformat(),
                }
                for s in signals
            ],
            "count": len(signals),
        }
        print(json.dumps(output, indent=2))

    elif command == "research":
        # Research companies from stdin
        from .linkt_client import get_linkt_client
        from .researcher import get_researcher

        if not stdin_data:
            print(json.dumps({"error": "No input data"}))
            return

        client = get_linkt_client(demo_mode=demo_mode)
        researcher = get_researcher(demo_mode=demo_mode)

        companies = []
        for sig in stdin_data.get("signals", []):
            company = client.enrich_company(sig["company_domain"])
            company.signal_type = sig["type"]
            company.signal_details = sig["details"]
            company = researcher.research_company(company)
            companies.append(company.model_dump())

        output = {"companies": companies, "count": len(companies)}
        print(json.dumps(output, indent=2))

    elif command == "generate-pages":
        # Generate landing pages from stdin
        from .page_generator import PageGenerator
        from .models import Company

        if not stdin_data:
            print(json.dumps({"error": "No input data"}))
            return

        generator = PageGenerator(
            your_company_name=os.getenv("YOUR_COMPANY_NAME", "Acme Inc"),
            your_value_prop=os.getenv("YOUR_VALUE_PROP", "AI automation"),
            cta_url=os.getenv("CTA_URL", "https://calendly.com/demo"),
        )

        pages = []
        for c in stdin_data.get("companies", []):
            company = Company(**c)
            page = generator.generate_page(company)
            generator.save_page(page)
            pages.append({
                "company": c,
                "slug": page.slug,
                "created_at": page.created_at.isoformat(),
            })

        output = {"pages": pages, "count": len(pages)}
        print(json.dumps(output, indent=2))

    elif command == "deploy":
        # Deploy pages
        from .deployer import get_deployer

        if not stdin_data:
            print(json.dumps({"error": "No input data"}))
            return

        deployer = get_deployer(platform=os.getenv("DEPLOY_PLATFORM", "local"))

        urls = []
        for p in stdin_data.get("pages", []):
            # In real impl, would deploy. For now, return local paths
            url = f"file://./output/{p['slug']}/index.html"
            urls.append({"slug": p["slug"], "url": url, "company": p["company"]})

        output = {"urls": urls, "count": len(urls)}
        print(json.dumps(output, indent=2))

    elif command == "draft-outreach":
        # Generate outreach drafts
        from .outreach import OutreachGenerator
        from .models import Company

        if not stdin_data:
            print(json.dumps({"error": "No input data"}))
            return

        generator = OutreachGenerator(
            sender_name=os.getenv("SENDER_NAME", "Alex"),
            sender_title=os.getenv("SENDER_TITLE", "Founder"),
            your_company_name=os.getenv("YOUR_COMPANY_NAME", "Acme Inc"),
        )

        drafts = []
        for item in stdin_data.get("urls", []):
            company = Company(**item["company"])
            outreach = generator.generate_outreach(company, item["url"])
            drafts.append({
                "company_name": company.name,
                "company_domain": company.domain,
                "page_url": item["url"],
                "email_subject": outreach.email_subject,
                "email_body": outreach.email_body,
                "linkedin_message": outreach.linkedin_message,
            })

        output = {
            "drafts": drafts,
            "count": len(drafts),
            "summary": "\n".join([f"- {d['company_name']}: {d['email_subject']}" for d in drafts]),
        }
        print(json.dumps(output, indent=2))

    elif command == "notify":
        # Send notifications
        from .notifications import get_notifier

        if not stdin_data:
            print(json.dumps({"error": "No input data"}))
            return

        notifier = get_notifier(platform=os.getenv("NOTIFY_PLATFORM", "mock"))
        count = stdin_data.get("count", 0)
        notifier.send_message(f"Signal-to-Site: Processed {count} leads")

        output = {"notified": True, "count": count}
        print(json.dumps(output, indent=2))

    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))


def _result_to_dict(result: PipelineResult) -> dict:
    """Convert PipelineResult to JSON-serializable dict."""
    return {
        "company_name": result.company.name,
        "company_domain": result.company.domain,
        "signal_type": result.company.signal_type,
        "signal_details": result.company.signal_details,
        "industry": result.company.industry,
        "location": result.company.location,
        "page_url": result.page_url,
        "page_slug": result.page.slug,
        "email_subject": result.outreach.email_subject,
        "email_body": result.outreach.email_body,
        "linkedin_message": result.outreach.linkedin_message,
        "email_sent": result.email_sent,
        "notified": result.notified,
    }


def _print_help(console: Console):
    """Print CLI help."""
    help_text = """
[bold]Usage:[/bold] signal-to-site [OPTIONS]

[bold]Options:[/bold]
  --demo              Run in demo mode with mock data
  --type TYPE         Filter signals by type (hiring, funding, tech_adoption)
  --domain DOMAIN     Process a single company by domain
  --signal TYPE       Signal type for single company mode
  --send-emails       Actually send outreach emails
  -h, --help          Show this help message

[bold]Examples:[/bold]
  # Run demo with mock data
  signal-to-site --demo

  # Process hiring signals
  signal-to-site --type hiring

  # Process a single company
  signal-to-site --domain techstartup.io --signal hiring

[bold]Environment Variables:[/bold]
  LINKT_API_KEY       Linkt API key
  OPENAI_API_KEY      OpenAI API key for content generation
  YOUR_COMPANY_NAME   Your company name
  YOUR_VALUE_PROP     Your value proposition
  SENDER_NAME         Outreach sender name
  SENDER_TITLE        Outreach sender title
  CTA_URL             Call-to-action URL
  NETLIFY_TOKEN       Netlify deploy token
  SLACK_WEBHOOK_URL   Slack notification webhook
"""
    console.print(help_text)


def _print_single_result(console: Console, result):
    """Print detailed result for single company."""
    console.print("\n[bold]Result:[/bold]\n")

    console.print(f"[cyan]Company:[/cyan] {result.company.name}")
    console.print(f"[cyan]Signal:[/cyan] {result.company.signal_type} - {result.company.signal_details}")
    console.print(f"[cyan]Industry:[/cyan] {result.company.industry or 'Unknown'}")

    console.print(f"\n[green]Landing Page:[/green] {result.page_url}")

    console.print(f"\n[yellow]Email Subject:[/yellow] {result.outreach.email_subject}")
    console.print(f"\n[yellow]Email Body:[/yellow]")
    console.print(Panel(result.outreach.email_body, border_style="dim"))

    if result.outreach.linkedin_message:
        console.print(f"\n[magenta]LinkedIn Message:[/magenta]")
        console.print(Panel(result.outreach.linkedin_message, border_style="dim"))

    console.print()


if __name__ == "__main__":
    main()
