Feature: Products API
  As a consumer of the Fake Store API
  I want to retrieve product data
  So that I can verify the catalogue is available

  Scenario: Get all products returns a non-empty list
    Given the API is available
    When I request GET "/products"
    Then the response status is 200
    And the response contains a list of products
    And every product contains the standard product fields

  Scenario: Get single product returns valid product data
    Given the API is available
    When I request GET "/products/1"
    Then the response status is 200
    And the response contains product with id 1
    And the product response has valid product data

  Scenario Outline: Get product by id returns valid product
    Given the API is available
    When I request GET "/products/<product_id>"
    Then the response status is 200
    And the response contains product with id <expected_id>

    Examples:
      | product_id | expected_id |
      | 1          | 1           |
      | 2          | 2           |
      | 3          | 3           |

  Scenario: Get products by category returns filtered results
    Given the API is available
    When I request GET "/products/category/electronics"
    Then the response status is 200
    And the response contains a list of products
    And all products in the response have category "electronics"
