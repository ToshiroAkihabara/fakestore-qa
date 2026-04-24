from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self._page_root = page.locator('[data-testid="page-root"]')

    def navigate(self, url: str):
        self.page.goto(url, wait_until='domcontentloaded')
        expect(self._page_root).to_be_visible()
