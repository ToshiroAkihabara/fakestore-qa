import allure


@allure.feature('Product Browsing')
class TestProductBrowsing:
    @allure.title('Home page displays a non-empty product list')
    def test_home_page_shows_products(self, home_page):
        home_page.wait_for_products()
        count = home_page.get_product_count()
        assert count > 0, 'No products displayed on the home page'

    @allure.title('Clicking a product opens the detail page')
    def test_click_product_opens_detail(self, home_page, product_page):
        home_page.wait_for_products()
        home_page.click_first_product()
        product_page.wait_for_detail()
        title = product_page.get_title()
        assert title, 'Product detail page has no title'
