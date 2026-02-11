@api @post_echo
Feature: POST Echo Endpoint Basic Form Data Tests
  As a QA engineer
  I want to validate the POST /post echo endpoint with form data
  So that I can ensure the API returns correct status, content type, and JSON structure

  Background:
    Given the API base URL is configured

  # ──────────────────────────────────────────────────────────
  # Scenario DQ-T9 — POST form data basic response validation
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify POST with form data returns 200 with JSON response
    When I send a POST request to "/post" with form data:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response status code should be 200
    And the response Content-Type should contain "application/json"
    And the response should be a JSON object
