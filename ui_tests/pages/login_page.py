from playwright.sync_api import Page, expect

from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._nav_login = page.locator('[data-testid="nav-login"]')
        self._form = page.locator('[data-testid="login-form"]')
        self._username_input = page.locator('[data-testid="login-username"]')
        self._password_input = page.locator('[data-testid="login-password"]')
        self._submit_button = page.locator('[data-testid="login-submit"]')
        self._success = page.locator('[data-testid="login-success"]')
        self._error = page.locator('[data-testid="login-error"]')
        self._logout_button = page.locator('[data-testid="logout-button"]')

    def open_login_form(self):
        self._nav_login.click()
        expect(self._form).to_be_visible()

    def fill_credentials(self, username: str, password: str):
        self._username_input.fill(username)
        self._password_input.fill(password)

    def submit(self):
        self._submit_button.click()

    def wait_for_success(self):
        expect(self._success).to_be_visible(timeout=15000)
        expect(self._logout_button).to_be_visible(timeout=15000)

    def wait_for_error(self):
        expect(self._error).to_be_visible(timeout=15000)
