import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.catalog_page import CatalogPage
from config.settings import Settings


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """Fixture providing an opened Login page instance."""
    lp = LoginPage(page)
    lp.open()
    return lp


@pytest.fixture(scope="function")
def catalog_page(page: Page) -> CatalogPage:
    """Fixture providing an authenticated session navigated to the Catalog."""
    lp = LoginPage(page)
    lp.open()
    lp.login(Settings.VALID_USERNAME, Settings.VALID_PASSWORD)

    catalog = CatalogPage(page)
    catalog.wait_for_catalog_load()
    return catalog