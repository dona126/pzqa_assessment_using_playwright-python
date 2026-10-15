import re
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from config.settings import Settings


class TestAuthentication:

    def test_tc_auth_01_successful_login(self, login_page: LoginPage, page: Page):
        """TC_AUTH_01: Successful login with valid credentials redirects away from login."""
        login_page.login(Settings.VALID_USERNAME, Settings.VALID_PASSWORD)
        expect(page).not_to_have_url(re.compile(r"/login/?$"))

    def test_tc_auth_02_incorrect_password(self, login_page: LoginPage, page: Page):
        """TC_AUTH_02: Login attempt with incorrect password remains on login page."""
        login_page.login(Settings.VALID_USERNAME, Settings.WRONG_PASSWORD)
        expect(page).to_have_url(re.compile(r"/login"))
        expect(login_page.submit_btn).to_be_visible()

    def test_tc_auth_03_unregistered_username(self, login_page: LoginPage, page: Page):
        """TC_AUTH_03: Login attempt with unregistered username remains on login page."""
        login_page.login(Settings.UNREGISTERED_USER, Settings.VALID_PASSWORD)
        expect(page).to_have_url(re.compile(r"/login"))
        expect(login_page.submit_btn).to_be_visible()

    def test_tc_auth_04_both_fields_blank(self, login_page: LoginPage, page: Page):
        """TC_AUTH_04: Login attempt with both fields blank triggers HTML5 required validation."""
        login_page.login("", "")
        assert login_page.is_username_required(), "Username field missing HTML5 'required' constraint"
        expect(page).to_have_url(re.compile(r"/login"))

    def test_tc_auth_05_username_filled_password_blank(self, login_page: LoginPage, page: Page):
        """TC_AUTH_05: Login attempt with username filled and password blank triggers HTML5 validation."""
        login_page.login(Settings.VALID_USERNAME, "")
        assert login_page.is_password_required(), "Password field missing HTML5 'required' constraint"
        expect(page).to_have_url(re.compile(r"/login"))

    def test_tc_auth_06_password_filled_username_blank(self, login_page: LoginPage, page: Page):
        """TC_AUTH_06: Login attempt with password filled and username blank triggers HTML5 validation."""
        login_page.login("", Settings.VALID_PASSWORD)
        assert login_page.is_username_required(), "Username field missing HTML5 'required' constraint"
        expect(page).to_have_url(re.compile(r"/login"))

    def test_tc_auth_07_password_field_input_masking(self, login_page: LoginPage):
        """TC_AUTH_07: Password field input masking (type='password')."""
        expect(login_page.password_input).to_have_attribute("type", "password")

    def test_tc_auth_08_direct_url_access_protected_routes(self, page: Page):
        """TC_AUTH_08: Direct URL access to protected routes in fresh unauthenticated context."""
        # Directly navigate to root / protected route
        page.goto(Settings.BASE_URL)

        # Unauthenticated access redirects to /login and displays the login submit button
        expect(page).to_have_url(re.compile(r"/login"))
        login_btn = page.locator("button[type='submit'], button:has-text('Sign in'), button:has-text('Login')").first
        expect(login_btn).to_be_visible()

    def test_tc_auth_09_successful_logout(self, login_page: LoginPage, page: Page):
        """TC_AUTH_09: Successful logout & session termination."""
        login_page.login(Settings.VALID_USERNAME, Settings.VALID_PASSWORD)
        
        # Ensure navigation completed to catalog
        expect(page).not_to_have_url(re.compile(r"/login/?$"))

        # Target the logout button specifically in header or navigation
        logout_btn = page.locator("header button:has-text('Logout'), button:has-text('Log out'), button:has-text('Sign out')").first
        expect(logout_btn).to_be_visible()
        logout_btn.click()

        # Session terminates and redirects back to /login
        expect(page).to_have_url(re.compile(r"/login"))
        expect(login_page.submit_btn).to_be_visible()