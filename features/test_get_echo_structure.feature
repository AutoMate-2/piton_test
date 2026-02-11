@api @get_echo
Feature: GET Echo Endpoint Structure Validation with Multiple Query Parameters
  As a QA engineer
  I want to validate the GET /get echo endpoint response structure
  So that I can ensure the response contains required contract keys

  Background:
    Given the API base URL is configured

  # ──────────────────────────────────────────────────────────
  # Scenario DQ-T17 — GET response structure with query params
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify GET response is a JSON object with required keys
    When I send a GET request to "/get" with query parameters:
      | key | value |
      | foo | bar   |
      | baz | value |
    Then the response should be a JSON object
    And the response JSON should contain key "args"
    And the response JSON should contain key "headers"
    And the response JSON should contain key "url"
