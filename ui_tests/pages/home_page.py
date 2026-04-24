from playwright.sync_api import Page, expect

from .base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._product_cards = page.locator('[data-testid="product-card"]')
        self._add_to_cart_buttons = page.locator('[data-testid="add-to-cart-button"]')
        self._view_buttons = page.locator('[data-testid="view-product-button"]')
        self._products_error = page.locator('[data-testid="products-error"]')

    def wait_for_products(self):
        expect(self._products_error).to_have_count(0)
        expect(self._product_cards.first).to_be_visible(timeout=15000)

    def get_product_count(self) -> int:
        return self._product_cards.count()

    def click_first_product(self):
        expect(self._view_buttons.first).to_be_visible()
        self._view_buttons.first.click()

    def add_first_product_to_cart(self):
        expect(self._add_to_cart_buttons.first).to_be_visible()
        self._add_to_cart_buttons.first.click()
