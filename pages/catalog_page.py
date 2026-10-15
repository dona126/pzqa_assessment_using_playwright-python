import re
from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage

class CatalogPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Verified Header Elements
        self.brand_pz_qa: Locator = page.locator("header h1:has-text('PZ QA')")
        self.brand_product_catalog: Locator = page.locator("header p:has-text('Product catalog')")
        self.cart_summary: Locator = page.get_by_test_id("cart-summary")
        self.cart_badge: Locator = page.get_by_test_id("cart-count")
        self.logout_btn: Locator = page.get_by_test_id("logout-button")

        # Section Banner & Subheading
        self.main_heading: Locator = page.locator("#products-heading")
        self.subheading: Locator = page.locator("section[aria-labelledby='products-heading'] p").first
        self.items_available_text: Locator = page.locator("p:has-text('items available')").first

        # Product Grid & Cards
        self.products_list: Locator = page.get_by_test_id("products-list")
        self.product_cards: Locator = page.locator("[data-testid='products-list'] article")

    def wait_for_catalog_load(self):
        """Ensure the product list and header are rendered in the DOM."""
        self.main_heading.wait_for(state="visible", timeout=10000)
        self.products_list.wait_for(state="visible", timeout=10000)
        self.product_cards.first.wait_for(state="attached", timeout=10000)

    def get_product_card(self, index: int = 0) -> Locator:
        return self.product_cards.nth(index)

    def get_product_title(self, card: Locator) -> str:
        return card.locator("h3").first.inner_text().strip()

    def get_product_price(self, card: Locator) -> str:
        return card.locator("[data-testid^='product-price-']").first.inner_text().strip()

    def get_add_to_cart_btn(self, card: Locator) -> Locator:
        return card.locator("[data-testid^='add-to-cart-']").first

    def get_increment_btn(self, card: Locator) -> Locator:
        return card.locator(
            "[data-testid*='increment'], [data-testid*='plus'], button:has-text('+'), button:has(svg):last-of-type"
        ).first

    def get_decrement_btn(self, card: Locator) -> Locator:
        return card.locator(
            "[data-testid*='decrement'], [data-testid*='minus'], button:has-text('-'), button:has-text('−'), button:has(svg):first-of-type"
        ).first

    def get_card_quantity(self, card: Locator) -> int:
        # Direct locator from the verified HTML data-testid
        qty_elem = card.locator("[data-testid^='product-quantity-']").first
        qty_elem.wait_for(state="visible", timeout=5000)
        return int(qty_elem.inner_text().strip())

    def get_available_count_from_banner(self) -> int:
        text = self.items_available_text.inner_text()
        match = re.search(r"(\d+)\s+items\s+available", text)
        return int(match.group(1)) if match else 0

    def add_product_to_cart(self, index: int = 0):
        card = self.get_product_card(index)
        self.get_add_to_cart_btn(card).click()
        self.page.wait_for_timeout(400) 