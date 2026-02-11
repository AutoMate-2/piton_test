@api @post_echo
Feature: POST Echo Endpoint Contract Key Tests
  As a QA engineer
  I want to validate the POST /post echo endpoint response structure
  So that I can ensure the API contract keys remain stable

  Background:
    Given the API base URL is configured

  # ──────────────────────────────────────────────────────────
  # Scenario DQ-T11 — POST form data contract key validation
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify POST with form data returns JSON with required contract keys
    When I send a POST request to "/post" with form data:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response should be a JSON object
    And the response JSON should contain key "form"
    And the response JSON should contain key "headers"
    And the response JSON should contain key "url"
