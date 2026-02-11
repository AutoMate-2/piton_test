@api @post_echo
Feature: POST Echo Endpoint Form Data Structure Tests
  As a QA engineer
  I want to validate the POST /post echo endpoint response structure
  So that I can ensure the response contains required contract keys

  Background:
    Given the API base URL is configured

  # ──────────────────────────────────────────────────────────
  # Scenario DQ-T11 — POST form data response structure validation
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify POST with form data returns JSON object with required keys
    When I send a POST request to "/post" with form data:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response should be a JSON object
    And the response JSON should contain key "form"
    And the response JSON should contain key "headers"
    And the response JSON should contain key "url"
