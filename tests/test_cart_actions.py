import pytest
from playwright.sync_api import expect
from pages.catalog_page import CatalogPage


class TestCartInteractions:

    def test_tc_act_01_initial_add_to_cart_counter_update(self, catalog_page: CatalogPage):
        """TC_ACT_01: First 'Add to Cart' updates header cart badge to 1."""
        card = catalog_page.get_product_card(0)
        add_btn = catalog_page.get_add_to_cart_btn(card)
        expect(add_btn).to_be_visible()

        add_btn.click()

        expect(catalog_page.cart_badge).to_be_visible()
        expect(catalog_page.cart_badge).to_have_text("1")

    def test_tc_act_02_subsequent_click_on_same_item_keeps_cart_badge_at_1(self, catalog_page: CatalogPage):
        """TC_ACT_02: Adding more of the same item does NOT increase distinct cart badge."""
        card = catalog_page.get_product_card(0)
        catalog_page.add_product_to_cart(0)

        expect(catalog_page.cart_badge).to_have_text("1")

        plus_btn = catalog_page.get_increment_btn(card)
        expect(plus_btn).to_be_visible()
        plus_btn.click()

        expect(catalog_page.cart_badge).to_have_text("1")

    def test_tc_act_03_product_card_quantity_increment(self, catalog_page: CatalogPage):
        """TC_ACT_03: Product card stepper increments item unit count by 1."""
        card = catalog_page.get_product_card(0)
        catalog_page.add_product_to_cart(0)

        initial_qty = catalog_page.get_card_quantity(card)
        qty_locator = card.locator("[data-testid^='product-quantity-']").first

        plus_btn = catalog_page.get_increment_btn(card)
        expect(plus_btn).to_be_visible()
        plus_btn.click()

        expect(qty_locator).to_have_text(str(initial_qty + 1))

    def test_tc_act_04_product_card_quantity_decrement(self, catalog_page: CatalogPage):
        """TC_ACT_04: Product card stepper decrements item unit count by 1 when qty >= 2."""
        card = catalog_page.get_product_card(0)

        # 1. Add product to cart
        add_btn = catalog_page.get_add_to_cart_btn(card)
        add_btn.click()

        # 2. Wait for quantity badge to show 1
        qty_locator = card.locator("[data-testid^='product-quantity-']").first
        expect(qty_locator).to_have_text("2")

        # 3. Click increment button
        plus_btn = catalog_page.get_increment_btn(card)
        expect(plus_btn).to_be_visible()
        plus_btn.click()
        expect(qty_locator).to_have_text("3")

        # 4. Click decrement button
        minus_btn = catalog_page.get_decrement_btn(card)
        expect(minus_btn).to_be_visible()
        minus_btn.click()

        # 5. Quantity returns to 1
        expect(qty_locator).to_have_text("2")

    def test_tc_act_05_catalog_view_item_decrement_keeps_cart_badge_at_1(self, catalog_page: CatalogPage):
        """TC_ACT_05: Decrementing units of the same item retains cart badge count."""
        card = catalog_page.get_product_card(0)

        # 1. Add product to cart
        add_btn = catalog_page.get_add_to_cart_btn(card)
        add_btn.click()

        # 2. Wait for quantity 1
        qty_locator = card.locator("[data-testid^='product-quantity-']").first
        expect(qty_locator).to_have_text("2")

        # 3. Increment
        plus_btn = catalog_page.get_increment_btn(card)
        expect(plus_btn).to_be_visible()
        plus_btn.click()
        expect(qty_locator).to_have_text("3")

        # 4. Decrement
        minus_btn = catalog_page.get_decrement_btn(card)
        expect(minus_btn).to_be_visible()
        minus_btn.click()

        # 5. Verify quantity is 2 and distinct cart count stays 1
        expect(qty_locator).to_have_text("2")
        expect(catalog_page.cart_badge).to_have_text("1")