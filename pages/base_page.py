from playwright.sync_api import Page, Locator, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url, wait_until="networkidle")

    def get_url(self) -> str:
        return self.page.url

    def wait_for_visible(self, locator: Locator):
        expect(locator).to_be_visible()

    def get_element_text(self, locator: Locator) -> str:
        return locator.inner_text().strip()