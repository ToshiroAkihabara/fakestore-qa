from behave import then


@then('the cart has an id')
def step_cart_has_id(context):
    data = context.response.json()
    assert 'id' in data, 'Cart has no id field'


@then('the cart has a list of products')
def step_cart_has_products(context):
    data = context.response.json()
    assert 'products' in data, 'Cart has no products field'
    assert isinstance(data['products'], list), 'Cart products is not a list'


@then('the response contains a list of carts')
def step_response_is_cart_list(context):
    data = context.response.json()
    assert isinstance(data, list) and data, 'Response is not a non-empty list'
