from playwright.sync_api import Page, expect

from .base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._detail = page.locator('[data-testid="product-detail"]')
        self._title = page.locator('[data-testid="product-title"]')
        self._price = page.locator('[data-testid="product-price"]')
        self._add_button = page.locator('[data-testid="add-to-cart-button"]')

    def wait_for_detail(self):
        expect(self._detail).to_be_visible(timeout=15000)

    def get_title(self) -> str:
        return (self._title.text_content() or '').strip()

    def get_price(self) -> str:
        return (self._price.text_content() or '').strip()

    def add_to_cart(self):
        expect(self._add_button).to_be_visible()
        self._add_button.click()
