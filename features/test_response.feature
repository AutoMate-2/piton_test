@api @get_echo
Feature: GET Echo Endpoint Contract Tests
  As a QA engineer
  I want to validate the GET /get echo endpoint
  So that I can ensure the API contract remains stable

  Background:
    Given the API base URL is configured

  # ──────────────────────────────────────────────────────────
  # Scenario 1 — Happy-path status & content-type
  # ──────────────────────────────────────────────────────────
  @smoke @positive
  Scenario: Verify successful response status and content type
    When I send a GET request to "/get" with query parameters:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response status code should be 200
    And the response Content-Type should contain "application/json"

  # ──────────────────────────────────────────────────────────
  # Scenario 2 — Response body structure (contract keys)
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify response body contains required contract keys
    When I send a GET request to "/get" with query parameters:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response should be a JSON object
    And the response JSON should contain key "args"
    And the response JSON should contain key "headers"
    And the response JSON should contain key "url"

  # ──────────────────────────────────────────────────────────
  # Scenario 3 — Query params echoed back correctly
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify query parameters are echoed in the args object
    When I send a GET request to "/get" with query parameters:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response status code should be 200
    And the JSON key "args.foo1" should equal "bar1"
    And the JSON key "args.foo2" should equal "bar2"

  # ──────────────────────────────────────────────────────────
  # Scenario 4 — JSON schema validation (full contract)
  # ──────────────────────────────────────────────────────────
  @contract @schema
  Scenario: Verify response matches the expected JSON schema
    When I send a GET request to "/get" with query parameters:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response status code should be 200
    And the response should match the GET echo JSON schema

  # ──────────────────────────────────────────────────────────
  # Scenario 5 — Performance: response time under threshold
  # ──────────────────────────────────────────────────────────
  @performance @positive
  Scenario: Verify response time is within acceptable limits
    When I send a GET request to "/get" with query parameters:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response status code should be 200
    And the response time should be under 5000 milliseconds

  # ──────────────────────────────────────────────────────────
  # Scenario 6 — Response headers contain Date header
  # ──────────────────────────────────────────────────────────
  @contract @headers
  Scenario: Verify response includes standard HTTP headers
    When I send a GET request to "/get" with query parameters:
      | key  | value |
      | foo1 | bar1  |
    Then the response status code should be 200
    And the response should have header "Date"
    And the response should have header "Content-Type"

  # ──────────────────────────────────────────────────────────
  # Scenario 7 — Request with no query params
  # ──────────────────────────────────────────────────────────
  @edge @positive
  Scenario: Verify GET request works with no query parameters
    When I send a GET request to "/get" without query parameters
    Then the response status code should be 200
    And the response should be a JSON object
    And the JSON key "args" should be an empty object
