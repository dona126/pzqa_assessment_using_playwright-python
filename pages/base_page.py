from playwright.sync_api import Page, Response
from typing import Optional


class BasePage:
    """Base class for all Page Object Models providing common browser navigation."""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> Optional[Response]:
        """Navigate to a given URL and await DOM content load."""
        return self.page.goto(url, wait_until="domcontentloaded")

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def get_title(self) -> str:
        """Return document title."""
        return self.page.title()