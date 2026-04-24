import allure


@allure.feature('Cart')
class TestAddToCart:
    @allure.title('Adding a product to cart increases the cart count')
    def test_add_product_updates_cart_count(self, home_page, cart_page):
        home_page.wait_for_products()
        count_before = cart_page.get_cart_count()
        home_page.add_first_product_to_cart()
        count_after = cart_page.get_cart_count()
        assert count_after == count_before + 1, (
            'Cart count did not increase after adding a product'
        )
