import os

import allure
import pytest
from playwright.sync_api import sync_playwright

from ui_tests.pages.cart_page import CartPage
from ui_tests.pages.home_page import HomePage
from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.product_page import ProductPage

BASE_URL = os.getenv('UI_BASE_URL', 'http://localhost:3000')
HEADLESS = os.getenv('PLAYWRIGHT_HEADLESS', 'true').lower() != 'false'


@pytest.fixture(scope='session')
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=HEADLESS)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context(viewport={'width': 1440, 'height': 960})
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def home_page(page):
    home_page = HomePage(page)
    home_page.navigate(BASE_URL)
    return home_page


@pytest.fixture
def product_page(page):
    return ProductPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def login_page(page):
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    return login_page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        page = item.funcargs.get('page')

        if page:
            screenshot = page.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name='failure-screenshot',
                attachment_type=allure.attachment_type.PNG,
            )
