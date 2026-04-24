from behave import given, when


@given('the API is available')
def step_api_available(context):
    response = context.session.get(f'{context.base_url}/products/1', timeout=context.timeout)
    assert response.status_code == 200, 'Fake Store API is not available'


@when('I request GET "{path}"')
def step_request_get(context, path):
    context.response = context.session.get(
        f'{context.base_url}{path}',
        timeout=context.timeout,
    )