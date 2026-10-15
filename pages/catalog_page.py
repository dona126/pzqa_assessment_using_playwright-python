import re
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from config.settings import Settings


class CatalogPage(BasePage):
    """Encapsulates locators and operations for the Product Catalog / PLP."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Header & Brand
        self.brand_pz_qa: Locator = page.locator("header h1, header span:has-text('PZ QA')").first
        self.brand_product_catalog: Locator = page.locator("header :has-text('Product catalog')").first
        self.cart_summary: Locator = page.locator(
            "[data-testid='cart-summary'], header :has-text('Cart'), header a[href*='cart']"
        ).first
        self.cart_badge: Locator = page.locator(
            "[data-testid='cart-badge'], [data-testid='cart-count'], header span.rounded-full"
        ).first
        self.logout_btn: Locator = page.locator("button:has-text('Log out'), button:has-text('Sign out')").first

        # Headings & Banner
        self.main_heading: Locator = page.locator("#products-heading, h1:has-text('Products')").first
        self.subheading: Locator = page.locator(
            "p:has-text('Add items with the stepper'), [data-testid='products-subheading']"
        ).first
        self.items_available_banner: Locator = page.locator(":has-text('items available')").first

        # Product Grid
        self.product_cards: Locator = page.locator(
            "[data-testid^='product-card-'], .grid > div:has(button)"
        )

    def wait_for_catalog_load(self):
        """Awaits core catalog elements to mount and render."""
        self.main_heading.wait_for(state="visible", timeout=10000)
        self.product_cards.first.wait_for(state="visible", timeout=10000)

    def get_available_count_from_banner(self) -> int:
        """Parse total items available declared in the banner."""
        text = self.items_available_banner.inner_text().strip()
        match = re.search(r"(\d+)\s+items?\s+available", text, re.IGNORECASE)
        return int(match.group(1)) if match else 0

    def get_product_card(self, index: int) -> Locator:
        return self.product_cards.nth(index)

    def get_product_title(self, card: Locator) -> str:
        title_el = card.locator("[data-testid*='title'], h3, p.font-semibold").first
        return title_el.inner_text().strip() if title_el.count() > 0 else ""

    def get_product_price(self, card: Locator) -> str:
        price_el = card.locator("[data-testid*='price']").first
        return price_el.inner_text().strip() if price_el.count() > 0 else ""

    def get_add_to_cart_btn(self, card: Locator) -> Locator:
        return card.locator("[data-testid^='add-to-cart-'], button:has-text('Add to cart')").first

    def get_increment_btn(self, card: Locator) -> Locator:
        return card.locator("[data-testid^='cart-increase-'], button[aria-label*='Increase' i]").first

    def get_decrement_btn(self, card: Locator) -> Locator:
        return card.locator("[data-testid^='cart-decrease-'], button[aria-label*='Decrease' i]").first

    def get_card_quantity(self, card: Locator) -> int:
        qty_el = card.locator("[data-testid^='product-quantity-']").first
        return int(qty_el.inner_text().strip()) if qty_el.count() > 0 else 0

    def add_product_to_cart(self, index: int):
        card = self.get_product_card(index)
        add_btn = self.get_add_to_cart_btn(card)
        if add_btn.is_visible():
            add_btn.click()