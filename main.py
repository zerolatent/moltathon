"""
Signal-to-Site: GTM Signal-to-Outreach Pipeline

Demo runner - shows the full pipeline in action with mock data.
"""

from signal_to_site.cli import main as cli_main


def main():
    """Run the Signal-to-Site pipeline."""
    cli_main()


def demo():
    """
    Run a quick demo showing the pipeline capabilities.

    This uses mock data to demonstrate the flow without requiring API keys.
    """
    from rich.console import Console
    from rich.panel import Panel

    from signal_to_site.pipeline import SignalToSitePipeline, PipelineConfig

    console = Console()

    console.print("\n")
    console.print(
        Panel.fit(
            "[bold blue]Signal-to-Site Demo[/bold blue]\n\n"
            "[dim]Demonstrating: Linkt Signal → Research → Landing Page → Outreach[/dim]",
            border_style="blue",
        )
    )

    # Create demo config
    config = PipelineConfig(
        your_company_name="SalesBot AI",
        your_value_prop="AI-powered sales automation that books 3x more meetings",
        sender_name="Sarah",
        sender_title="Head of Growth",
        cta_url="https://calendly.com/salesbot-demo",
        demo_mode=True,
        deploy_platform="local",
        notify_platform="mock",
        max_signals=3,
    )

    # Run pipeline
    pipeline = SignalToSitePipeline(config)
    results = pipeline.run(signal_type="hiring")

    # Show what was generated
    console.print("\n[bold]What just happened:[/bold]")
    console.print("1. Detected 3 hiring signals from Linkt (mock data)")
    console.print("2. Researched each company for pain points and value props")
    console.print("3. Generated personalized landing pages")
    console.print("4. Created tailored outreach emails")
    console.print("5. Sent notifications (mock)")

    console.print("\n[bold green]Check the ./output folder for generated pages![/bold green]")
    console.print("[dim]Open: file://./output/index.html[/dim]\n")

    return results


if __name__ == "__main__":
    import sys

    if "--demo" in sys.argv or len(sys.argv) == 1:
        demo()
    else:
        main()
