import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from config.settings import Settings

class TestAuthentication:

    def test_tc_auth_01_successful_login(self, login_page: LoginPage, page: Page):
        """TC_AUTH_01: Successful login with valid credentials."""
        login_page.login(Settings.VALID_USERNAME, Settings.VALID_PASSWORD)
        
        # Wait for navigation away from /login
        page.wait_for_url(lambda u: "/login" not in u, timeout=7000)
        assert "/login" not in page.url, f"Expected redirect away from login, but stayed on {page.url}"

    def test_tc_auth_02_incorrect_password(self, login_page: LoginPage, page: Page):
        """TC_AUTH_02: Login attempt with incorrect password."""
        login_page.login(Settings.VALID_USERNAME, Settings.WRONG_PASSWORD)
        page.wait_for_timeout(600)
        assert "/login" in page.url

    def test_tc_auth_03_unregistered_username(self, login_page: LoginPage, page: Page):
        """TC_AUTH_03: Login attempt with unregistered username."""
        login_page.login(Settings.UNREGISTERED_USER, Settings.VALID_PASSWORD)
        page.wait_for_timeout(600)
        assert "/login" in page.url

    def test_tc_auth_04_both_fields_blank(self, login_page: LoginPage, page: Page):
        """TC_AUTH_04: Login attempt with both fields blank (HTML5 required)."""
        login_page.login("", "")
        assert login_page.is_username_required() or "/login" in page.url

    def test_tc_auth_05_username_filled_password_blank(self, login_page: LoginPage, page: Page):
        """TC_AUTH_05: Login attempt with username filled and password blank."""
        login_page.login(Settings.VALID_USERNAME, "")
        assert login_page.is_password_required() or "/login" in page.url

    def test_tc_auth_06_password_filled_username_blank(self, login_page: LoginPage, page: Page):
        """TC_AUTH_06: Login attempt with password filled and username blank."""
        login_page.login("", Settings.VALID_PASSWORD)
        assert login_page.is_username_required() or "/login" in page.url

    def test_tc_auth_07_password_field_input_masking(self, login_page: LoginPage):
        """TC_AUTH_7: Password field input masking (type='password')."""
        assert login_page.get_password_field_type() == "password", "Password characters are not masked!"

    def test_tc_auth_08_direct_url_access_protected_routes(self, page: Page):
        """TC_AUTH_8: Direct URL access to protected routes in fresh context."""
        page.goto(Settings.BASE_URL)
        page.wait_for_load_state("networkidle")
        assert "/login" in page.url or page.locator("button:has-text('Sign in')").is_visible()

    def test_tc_auth_09_successful_logout(self, login_page: LoginPage, page: Page):
        """TC_AUTH_9: Successful logout & session termination."""
        login_page.login(Settings.VALID_USERNAME, Settings.VALID_PASSWORD)
        page.wait_for_load_state("networkidle")

        logout_btn = page.locator("button:has-text('Logout'), button:has-text('Sign out')").first
        if logout_btn.is_visible():
            logout_btn.click()
            page.wait_for_load_state("networkidle")
            assert "/login" in page.url or page.locator("button:has-text('Sign in')").is_visible()