@api @get_echo
Feature: GET Echo Endpoint URL Query Parameter Validation
  As a QA engineer
  I want to validate the GET /get echo endpoint URL contains query parameters
  So that I can ensure the API correctly reflects the full request URL

  Background:
    Given the API base URL is configured

  # ──────────────────────────────────────────────────────────
  # Scenario DQ-T18 — URL contains query parameters
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify GET response URL contains host and query parameters
    When I send a GET request to "/get" with query parameters:
      | key | value |
      | foo | bar   |
      | baz | value |
    Then the response status code should be 200
    And the JSON key "url" should contain "postman-echo.com/get"
    And the JSON key "url" should contain "foo=bar"
    And the JSON key "url" should contain "baz=value"
