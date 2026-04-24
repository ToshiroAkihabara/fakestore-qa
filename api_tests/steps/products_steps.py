from behave import then


def _assert_valid_product_contract(product):
    assert isinstance(product['id'], int), 'Product id is not an integer'
    assert isinstance(product['title'], str) and product['title'].strip(), (
        'Product title is empty or not a string'
    )
    assert isinstance(product['price'], (int, float)) and product['price'] > 0, (
        'Product price is not a positive number'
    )
    assert isinstance(product['category'], str) and product['category'].strip(), (
        'Product category is empty or not a string'
    )


@then('the response status is {status_code:d}')
def step_response_status(context, status_code):
    assert context.response is not None, 'Response is empty'
    assert context.response.status_code == status_code, (
        f'Expected status {status_code}, got {context.response.status_code}'
    )


@then('the response contains a list of products')
def step_response_contains_products(context):
    data = context.response.json()
    assert isinstance(data, list), 'Response is not a list'
    assert data, 'Product list is empty'


@then('every product contains the standard product fields')
def step_products_have_standard_fields(context):
    data = context.response.json()
    required_fields = {'id', 'title', 'price', 'category'}
    for product in data:
        missing = required_fields.difference(product.keys())
        assert not missing, (
            f"Product {product.get('id')} is missing fields: {sorted(missing)}"
        )


@then('the response contains product with id {product_id:d}')
def step_response_contains_product(context, product_id):
    data = context.response.json()
    assert data['id'] == product_id, f"Expected id {product_id}, got {data['id']}"


@then('the product response has valid product data')
def step_product_response_has_valid_data(context):
    data = context.response.json()
    _assert_valid_product_contract(data)


@then('all products in the response have category "{category}"')
def step_all_products_in_category(context, category):
    data = context.response.json()
    assert isinstance(data, list) and data, 'Response is not a non-empty list'
    for product in data:
        assert product['category'] == category, (
            f"Expected category '{category}', got '{product['category']}'"
        )
