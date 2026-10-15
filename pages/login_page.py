from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage
from config.settings import Settings

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators from verified HTML
        self.login_page_container: Locator = page.get_by_test_id("login-page")
        self.login_form: Locator = page.get_by_test_id("login-form")
        self.email_input: Locator = page.get_by_test_id("login-email")
        # Alias so tests referring to username or email both work seamlessly
        self.username_input: Locator = self.email_input
        self.password_input: Locator = page.get_by_test_id("login-password")
        self.submit_btn: Locator = page.get_by_test_id("login-submit")
        self.error_prompt: Locator = page.locator("[role='alert'], .text-red-500, .text-red-600, form p.text-sm")

    def open(self):
        self.navigate(Settings.LOGIN_URL)

    def login(self, email: str = "", password: str = ""):
        self.email_input.clear()
        if email:
            self.email_input.fill(email)

        self.password_input.clear()
        if password:
            self.password_input.fill(password)

        self.submit_btn.click()

    def get_password_field_type(self) -> str:
        return self.password_input.get_attribute("type") or ""

    def is_email_required(self) -> bool:
        return self.email_input.evaluate("el => el.validity.valueMissing")

    # Method alias so tests calling is_username_required succeed
    def is_username_required(self) -> bool:
        return self.is_email_required()

    def is_password_required(self) -> bool:
        return self.password_input.evaluate("el => el.validity.valueMissing")