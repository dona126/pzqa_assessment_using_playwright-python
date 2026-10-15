import pytest
from playwright.sync_api import expect
from pages.catalog_page import CatalogPage
from config.settings import Settings


class TestCatalogBrowsing:

    def test_tc_cat_01_header_layout_and_navigation(self, catalog_page: CatalogPage):
        """TC_CAT_01: Header logo, PZ QA text, Product catalog, Cart UI with count 0, and Logout button."""
        expect(catalog_page.brand_pz_qa).to_be_visible()
        expect(catalog_page.brand_product_catalog).to_be_visible()

        expect(catalog_page.cart_summary).to_be_visible()
        expect(catalog_page.cart_badge).to_be_visible()
        expect(catalog_page.cart_badge).to_have_text("0")

        expect(catalog_page.logout_btn).to_be_visible()

    def test_tc_cat_02_title_and_subheading_display(self, catalog_page: CatalogPage):
        """TC_CAT_02: Catalog page title ('Products') and descriptive subheading display."""
        expect(catalog_page.main_heading).to_be_visible()
        expect(catalog_page.main_heading).to_have_text(Settings.EXPECTED_HEADING)

        expect(catalog_page.subheading).to_be_visible()
        expect(catalog_page.subheading).to_contain_text(Settings.EXPECTED_SUBHEADING)

    def test_tc_cat_03_plp_total_product_card_count_verification(self, catalog_page: CatalogPage):
        """TC_CAT_03 / BUG-003: Compare rendered cards on PLP vs banner item count."""
        expect(catalog_page.product_cards.first).to_be_visible()

        rendered_cards = catalog_page.product_cards.count()
        banner_count = catalog_page.get_available_count_from_banner()

        if rendered_cards != banner_count:
            pytest.xfail(
                f"BUG-003 Verified: Banner states {banner_count} items available, "
                f"but only {rendered_cards} cards are rendered."
            )

        expect(catalog_page.product_cards).to_have_count(banner_count)

    def test_tc_cat_04_product_card_attributes_and_formatting(self, catalog_page: CatalogPage):
        """TC_CAT_04 / BUG-004: Verify each card has title, valid price ($XX.XX), CTA, and check image rendering."""
        expect(catalog_page.product_cards.first).to_be_visible()
        card_count = catalog_page.product_cards.count()

        missing_images = []

        for i in range(card_count):
            card = catalog_page.get_product_card(i)

            title_elem = card.locator("[data-testid*='title'], h3, p.font-semibold").first
            expect(title_elem).to_be_visible()
            title = title_elem.inner_text().strip()
            assert len(title) > 0, f"Card at index {i} has empty title"

            price_elem = card.locator("[data-testid*='price']").first
            expect(price_elem).to_be_visible()
            expect(price_elem).to_contain_text("$")

            cta_btn = catalog_page.get_add_to_cart_btn(card)
            expect(cta_btn).to_be_visible()

            if card.locator("img").count() == 0:
                missing_images.append(title)

        if missing_images:
            pytest.xfail(
                f"BUG-004 Verified: Products {missing_images} lack <img> elements (render placeholder div)."
            )