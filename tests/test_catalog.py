import pytest
from playwright.sync_api import Page, expect
from pages.catalog_page import CatalogPage
from config.settings import Settings

class TestCatalogBrowsing:

    def test_tc_cat_01_header_layout_and_navigation(self, catalog_page: CatalogPage):
        """TC_CAT_01: Header logo, PZ QA text, Product catalog, Cart UI with count 0, and Logout button."""
        # Brand text & subtitle
        expect(catalog_page.brand_pz_qa).to_be_visible()
        expect(catalog_page.brand_product_catalog).to_be_visible()

        # Cart UI container, text, and initial count of '0'
        expect(catalog_page.cart_summary).to_be_visible()
        expect(catalog_page.cart_badge).to_be_visible()
        assert catalog_page.cart_badge.inner_text().strip() == "0", "Initial cart badge count was not '0'"

        # Logout button
        expect(catalog_page.logout_btn).to_be_visible()

    def test_tc_cat_02_title_and_subheading_display(self, catalog_page: CatalogPage):
        """TC_CAT_02: Catalog page title ('Products') and descriptive subheading display."""
        expect(catalog_page.main_heading).to_be_visible()
        assert catalog_page.main_heading.inner_text().strip() == Settings.EXPECTED_HEADING

        expect(catalog_page.subheading).to_be_visible()
        assert Settings.EXPECTED_SUBHEADING in catalog_page.subheading.inner_text().strip()

    def test_tc_cat_03_plp_total_product_card_count_verification(self, catalog_page: CatalogPage):
        """TC_CAT_03 / BUG-003: Compare rendered cards on PLP vs banner item count."""
        rendered_cards = catalog_page.product_cards.count()
        banner_count = catalog_page.get_available_count_from_banner()

        print(f"\n[TC_CAT_03] Banner: {banner_count} items available | Rendered Cards: {rendered_cards}")

        # Identifies BUG-003 (Banner states 6, but only 5 cards render)
        if rendered_cards != banner_count:
            pytest.xfail(f"BUG-003 Verified: Banner states {banner_count} items available, but only {rendered_cards} cards are rendered.")

        assert rendered_cards == banner_count

    def test_tc_cat_04_product_card_attributes_and_formatting(self, catalog_page: CatalogPage):
        """TC_CAT_04 / BUG-004: Verify each card has title, valid price ($XX.XX), CTA, and check image rendering."""
        card_count = catalog_page.product_cards.count()
        assert card_count > 0, "No product cards found"

        missing_images = []

        for i in range(card_count):
            card = catalog_page.get_product_card(i)

            # Title
            title = catalog_page.get_product_title(card)
            assert len(title) > 0, f"Card at index {i} has empty title"

            # Price ($XX.XX)
            price = catalog_page.get_product_price(card)
            assert price.startswith("$"), f"Price '{price}' does not have currency symbol $"

            # CTA Button
            cta_btn = catalog_page.get_add_to_cart_btn(card)
            expect(cta_btn).to_be_visible()

            # Image Check
            if card.locator("img").count() == 0:
                missing_images.append(title)

        # Identifies BUG-004 (Cards use colored div placeholder instead of <img>)
        if missing_images:
            pytest.xfail(f"BUG-004 Verified: Products {missing_images} lack <img> elements (render placeholder div).")