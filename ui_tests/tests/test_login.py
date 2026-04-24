import allure

VALID_USERNAME = 'mor_2314'
VALID_PASSWORD = '83r5^_'


@allure.feature('Authentication')
class TestLogin:
    @allure.title('User can log in with valid credentials')
    def test_login_valid_credentials(self, login_page):
        login_page.open_login_form()
        login_page.fill_credentials(VALID_USERNAME, VALID_PASSWORD)
        login_page.submit()
        login_page.wait_for_success()

    @allure.title('User sees an error with invalid credentials')
    def test_login_invalid_credentials(self, login_page):
        login_page.open_login_form()
        login_page.fill_credentials('wrong_user', 'wrong_pass')
        login_page.submit()
        login_page.wait_for_error()
