from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from config.settings import Settings


class LoginPage(BasePage):
    """Encapsulates locators and interactions for the Login route."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input: Locator = page.locator(
            "input[type='text'], input[type='email'], input#username, input[name='username']"
        ).first
        self.password_input: Locator = page.locator("input#password, input[name='password']").first
        self.submit_btn: Locator = page.locator("button[type='submit'], button:has-text('Sign in'), button:has-text('Login'), [data-testid='login-submit']").first
        self.error_message: Locator = page.locator(
            "[role='alert'], .error, [data-testid='login-error'], p.text-red-500"
        ).first

    def open(self):
        """Navigate directly to the Login page."""
        self.navigate(Settings.LOGIN_URL)

    def login(self, username: str, password: str):
        """Fill credentials and submit the form."""
        if username:
            self.username_input.fill(username)
        else:
            self.username_input.clear()

        if password:
            self.password_input.fill(password)
        else:
            self.password_input.clear()

        self.submit_btn.click()

    def is_username_required(self) -> bool:
        """Check HTML5 'required' constraint on username input."""
        return self.username_input.evaluate("el => el.required")

    def is_password_required(self) -> bool:
        """Check HTML5 'required' constraint on password input."""
        return self.password_input.evaluate("el => el.required")

    def get_password_field_type(self) -> str:
        """Verify password input masking type attribute."""
        return self.password_input.get_attribute("type") or ""