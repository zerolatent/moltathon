"""Headless browser automation for website research."""

import os
import re
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class BrowserResearchResult:
    """Result of browser-based research on a company website."""

    domain: str
    title: str = ""
    tagline: str = ""
    description: str = ""
    primary_color: str = "#2563eb"  # Default blue
    secondary_color: str = "#1e293b"  # Default dark
    background_style: str = "light"  # "light" or "dark"
    customers: list[str] = None
    team_members: list[dict] = None
    text_content: str = ""
    screenshot_path: Optional[str] = None

    def __post_init__(self):
        if self.customers is None:
            self.customers = []
        if self.team_members is None:
            self.team_members = []


class HeadlessBrowser:
    """Headless browser for scraping websites with Playwright."""

    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._browser = None
        self._playwright = None

    async def __aenter__(self):
        from playwright.async_api import async_playwright
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=True)
        return self

    async def __aexit__(self, *args):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def research_company(self, domain: str) -> BrowserResearchResult:
        """
        Research a company website using headless browser.

        Visits the site, takes screenshot, extracts colors and content.
        """
        result = BrowserResearchResult(domain=domain)

        context = await self._browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()

        try:
            # Visit homepage
            url = f"https://{domain}"
            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Take screenshot
            slug = domain.replace(".", "-")
            screenshot_dir = self.output_dir / slug
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshot_dir / "homepage.png"
            await page.screenshot(path=str(screenshot_path), full_page=False)
            result.screenshot_path = str(screenshot_path)

            # Get page title
            result.title = await page.title() or ""

            # Extract text content
            result.text_content = await page.evaluate("""
                () => {
                    const elementsToRemove = document.querySelectorAll('script, style, nav, footer, header, iframe');
                    elementsToRemove.forEach(el => el.remove());
                    return document.body.innerText.slice(0, 10000);
                }
            """)

            # Extract tagline (usually h1 or hero text)
            result.tagline = await page.evaluate("""
                () => {
                    const h1 = document.querySelector('h1');
                    if (h1) return h1.innerText.trim();
                    const hero = document.querySelector('[class*="hero"] h1, [class*="hero"] h2, main h1');
                    if (hero) return hero.innerText.trim();
                    return '';
                }
            """) or ""

            # Extract colors from the page
            colors = await page.evaluate("""
                () => {
                    const colors = {
                        buttons: [],
                        backgrounds: [],
                        links: []
                    };

                    // Get button colors
                    document.querySelectorAll('button, a[class*="btn"], [class*="button"]').forEach(el => {
                        const style = window.getComputedStyle(el);
                        const bg = style.backgroundColor;
                        if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') {
                            colors.buttons.push(bg);
                        }
                    });

                    // Get body background
                    const bodyBg = window.getComputedStyle(document.body).backgroundColor;
                    colors.backgrounds.push(bodyBg);

                    // Get link colors
                    document.querySelectorAll('a').forEach(el => {
                        const style = window.getComputedStyle(el);
                        colors.links.push(style.color);
                    });

                    return colors;
                }
            """)

            # Parse colors
            if colors.get("buttons"):
                result.primary_color = self._rgb_to_hex(colors["buttons"][0])

            # Determine if dark mode
            if colors.get("backgrounds"):
                bg_color = colors["backgrounds"][0]
                result.background_style = self._is_dark_background(bg_color)
                if result.background_style == "dark":
                    result.secondary_color = "#ffffff"

            # Try to get customers/logos
            result.customers = await page.evaluate("""
                () => {
                    const customers = [];
                    // Look for customer logos or testimonials
                    document.querySelectorAll('[class*="customer"] img, [class*="logo"] img, [class*="client"] img').forEach(img => {
                        const alt = img.alt || img.title;
                        if (alt && alt.length < 50) customers.push(alt);
                    });
                    // Also check for customer names in text
                    document.querySelectorAll('[class*="customer"], [class*="testimonial"]').forEach(el => {
                        const text = el.innerText;
                        if (text && text.length < 100) customers.push(text.split('\\n')[0]);
                    });
                    return [...new Set(customers)].slice(0, 5);
                }
            """) or []

            # Try to visit about page for team info
            try:
                about_url = f"https://{domain}/about"
                await page.goto(about_url, wait_until="networkidle", timeout=15000)

                # Extract team members
                result.team_members = await page.evaluate("""
                    () => {
                        const team = [];
                        document.querySelectorAll('[class*="team"] [class*="member"], [class*="team"] [class*="person"], [class*="leadership"]').forEach(el => {
                            const name = el.querySelector('h3, h4, [class*="name"]')?.innerText;
                            const title = el.querySelector('[class*="title"], [class*="role"], p')?.innerText;
                            if (name) {
                                team.push({ name: name.trim(), title: title?.trim() || '' });
                            }
                        });
                        return team.slice(0, 5);
                    }
                """) or []

                # Get about page description
                about_text = await page.evaluate("""
                    () => {
                        const main = document.querySelector('main, [class*="about"], article');
                        if (main) return main.innerText.slice(0, 2000);
                        return document.body.innerText.slice(0, 2000);
                    }
                """)
                if about_text:
                    result.description = about_text[:500]

            except Exception:
                # About page doesn't exist or failed
                pass

        except Exception as e:
            print(f"Browser error for {domain}: {e}")
        finally:
            await context.close()

        return result

    def _rgb_to_hex(self, rgb_string: str) -> str:
        """Convert RGB string to hex color."""
        try:
            # Match rgb(r, g, b) or rgba(r, g, b, a)
            match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', rgb_string)
            if match:
                r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
                return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            pass
        return "#2563eb"  # Default blue

    def _is_dark_background(self, rgb_string: str) -> str:
        """Determine if background is dark or light."""
        try:
            match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', rgb_string)
            if match:
                r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
                # Calculate luminance
                luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                return "dark" if luminance < 0.5 else "light"
        except Exception:
            pass
        return "light"


def research_with_browser(domain: str, output_dir: str = "./output") -> BrowserResearchResult:
    """
    Synchronous wrapper for browser research.

    Usage:
        result = research_with_browser("stripe.com")
        print(result.primary_color)
    """
    import asyncio

    async def _research():
        async with HeadlessBrowser(output_dir) as browser:
            return await browser.research_company(domain)

    return asyncio.run(_research())
