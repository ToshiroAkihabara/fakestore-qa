from behave import then, when


@when('I POST to "{path}" with username "{username}" and password "{password}"')
def step_post_login(context, path, username, password):
    context.response = context.session.post(
        f'{context.base_url}{path}',
        json={'username': username, 'password': password},
        timeout=context.timeout,
    )


@then('the response contains a token')
def step_response_has_token(context):
    data = context.response.json()
    assert 'token' in data, f'No token in response: {data}'
    assert data['token'], 'Token is empty'
