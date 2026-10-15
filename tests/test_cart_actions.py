import pytest
from playwright.sync_api import Page, expect
from pages.catalog_page import CatalogPage


class TestCartInteractions:

    def test_tc_act_01_initial_add_to_cart_counter_update(self, catalog_page: CatalogPage, page: Page):
        """TC_ACT_01: First 'Add to Cart' updates header cart badge to 1."""
        card = catalog_page.get_product_card(0)
        add_btn = catalog_page.get_add_to_cart_btn(card)
        expect(add_btn).to_be_visible()

        add_btn.click()
        page.wait_for_timeout(400)

        expect(catalog_page.cart_badge).to_be_visible()
        badge_text = catalog_page.cart_badge.inner_text().strip()
        assert badge_text == "1", f"Expected header cart badge to be '1', got '{badge_text}'"

    def test_tc_act_02_subsequent_click_on_same_item_keeps_cart_badge_at_1(self, catalog_page: CatalogPage, page: Page):
        """TC_ACT_02: Adding more of the same item does NOT increase distinct cart badge."""
        card = catalog_page.get_product_card(0)
        catalog_page.add_product_to_cart(0)

        assert catalog_page.cart_badge.inner_text().strip() == "1"

        plus_btn = catalog_page.get_increment_btn(card)
        expect(plus_btn).to_be_visible()
        plus_btn.click()
        page.wait_for_timeout(400)

        badge_text = catalog_page.cart_badge.inner_text().strip()
        assert badge_text == "1", f"Cart badge incremented unexpectedly! Expected '1', got '{badge_text}'"

    def test_tc_act_03_product_card_quantity_increment(self, catalog_page: CatalogPage, page: Page):
        """TC_ACT_03: Product card stepper increments item unit count by 1."""
        card = catalog_page.get_product_card(0)
        catalog_page.add_product_to_cart(0)

        initial_qty = catalog_page.get_card_quantity(card)

        plus_btn = catalog_page.get_increment_btn(card)
        expect(plus_btn).to_be_visible()
        plus_btn.click()
        page.wait_for_timeout(400)

        new_qty = catalog_page.get_card_quantity(card)
        assert new_qty == initial_qty + 1, f"Expected card qty {initial_qty + 1}, got {new_qty}"

    def test_tc_act_04_product_card_quantity_decrement(self, catalog_page: CatalogPage, page: Page):
        """TC_ACT_04: Product card stepper decrements item unit count by 1 when qty >= 2."""
        card = catalog_page.get_product_card(0)
        catalog_page.add_product_to_cart(0)

        # Increment first so quantity reaches at least 2
        plus_btn = catalog_page.get_increment_btn(card)
        expect(plus_btn).to_be_visible()
        plus_btn.click()
        page.wait_for_timeout(400)

        qty_before = catalog_page.get_card_quantity(card)
        assert qty_before >= 2, f"Precondition failed: expected qty >= 2, got {qty_before}"

        # Click '-' once
        minus_btn = catalog_page.get_decrement_btn(card)
        expect(minus_btn).to_be_visible()
        minus_btn.click()
        page.wait_for_timeout(400)

        qty_after = catalog_page.get_card_quantity(card)
        assert qty_after == qty_before - 1, f"Expected card qty {qty_before - 1}, got {qty_after}"

    def test_tc_act_05_catalog_view_item_decrement_keeps_cart_badge_at_1(self, catalog_page: CatalogPage, page: Page):
        """TC_ACT_05: Decrementing units of the same item retains cart badge count."""
        card = catalog_page.get_product_card(0)
        catalog_page.add_product_to_cart(0)

        # Increase units to 2 so item is not removed when clicking '-'
        plus_btn = catalog_page.get_increment_btn(card)
        expect(plus_btn).to_be_visible()
        plus_btn.click()
        page.wait_for_timeout(400)

        # Tap '-' on the card
        minus_btn = catalog_page.get_decrement_btn(card)
        expect(minus_btn).to_be_visible()
        minus_btn.click()
        page.wait_for_timeout(400)

        # Cart badge in header still shows 1 distinct item
        badge_text = catalog_page.cart_badge.inner_text().strip()
        assert badge_text == "1", f"Expected header cart badge to stay '1', got '{badge_text}'"