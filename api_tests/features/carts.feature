Feature: Carts API
  As a user of the Fake Store
  I want to manage carts via the API
  So that I can verify cart operations work correctly

  Scenario: Get a single cart returns correct structure
    Given the API is available
    When I request GET "/carts/1"
    Then the response status is 200
    And the cart has an id
    And the cart has a list of products

  Scenario: Get all carts returns a non-empty list
    Given the API is available
    When I request GET "/carts"
    Then the response status is 200
    And the response contains a list of carts
