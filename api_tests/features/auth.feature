Feature: Authentication API
  As a user of the Fake Store
  I want to authenticate via the API
  So that I can access protected resources

  Scenario: Login with valid credentials returns a token
    Given the API is available
    When I POST to "/auth/login" with username "mor_2314" and password "83r5^_"
    Then the response status is 201
    And the response contains a token

  Scenario: Login with invalid credentials returns an error
    Given the API is available
    When I POST to "/auth/login" with username "invalid_user" and password "wrong_pass"
    Then the response status is 401
