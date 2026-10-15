import os
import sys
import pytest
from playwright.sync_api import Page

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.login_page import LoginPage
from pages.catalog_page import CatalogPage
from config.settings import Settings

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    lp = LoginPage(page)
    lp.open()
    return lp

@pytest.fixture
def catalog_page(page: Page) -> CatalogPage:
    lp = LoginPage(page)
    lp.open()
    lp.login(Settings.VALID_USERNAME, Settings.VALID_PASSWORD)
    
    # Wait for catalog page container and cards to mount
    catalog = CatalogPage(page)
    catalog.wait_for_catalog_load()
    return catalog