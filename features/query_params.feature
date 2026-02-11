@api @query_params
Feature: Valid Query Params Contract Tests
  As a QA engineer
  I want to validate the GET /get endpoint echoes query parameters correctly
  So that I can ensure query param handling remains stable

  Background:
    Given the API base URL is configured

  # ──────────────────────────────────────────────────────────
  # Scenario 1 — Status code and Content-Type exact match
  # ──────────────────────────────────────────────────────────
  @smoke @positive
  Scenario: Verify response returns 200 with correct Content-Type
    When I send a GET request to "/get" with query parameters:
      | key | value |
      | foo | bar   |
      | baz | value |
    Then the response status code should be 200
    And the response Content-Type should equal "application/json; charset=utf-8"

  # ──────────────────────────────────────────────────────────
  # Scenario 2 — Query params echoed back in args object
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify query parameters are correctly echoed in args
    When I send a GET request to "/get" with query parameters:
      | key | value |
      | foo | bar   |
      | baz | value |
    Then the response status code should be 200
    And the JSON key "args" should be of type "object"
    And the JSON key "args.foo" should equal "bar"
    And the JSON key "args.baz" should equal "value"

  # ──────────────────────────────────────────────────────────
  # Scenario 3 — Date header is present and valid
  # ──────────────────────────────────────────────────────────
  @contract @headers
  Scenario: Verify Date header exists and contains a valid date
    When I send a GET request to "/get" with query parameters:
      | key | value |
      | foo | bar   |
      | baz | value |
    Then the response status code should be 200
    And the response should have header "Date"
    And the response header "Date" should be a valid date

  # ──────────────────────────────────────────────────────────
  # Scenario 4 — Response body contract structure
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify response contains all required contract keys
    When I send a GET request to "/get" with query parameters:
      | key | value |
      | foo | bar   |
      | baz | value |
    Then the response should be a JSON object
    And the response JSON should contain key "args"
    And the response JSON should contain key "headers"
    And the response JSON should contain key "url"

  # ──────────────────────────────────────────────────────────
  # Scenario 5 — URL property reflects the request URL
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify the url property contains the original request URL
    When I send a GET request to "/get" with query parameters:
      | key | value |
      | foo | bar   |
      | baz | value |
    Then the response status code should be 200
    And the JSON key "url" should contain "postman-echo.com/get"
    And the JSON key "url" should contain "foo=bar"
    And the JSON key "url" should contain "baz=value"
