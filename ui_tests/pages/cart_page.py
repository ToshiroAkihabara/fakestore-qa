from playwright.sync_api import Page, expect

from .base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._cart_count = page.locator('[data-testid="cart-count"]')

    def get_cart_count(self) -> int:
        expect(self._cart_count).to_be_visible()
        return int((self._cart_count.text_content() or '0').strip())
