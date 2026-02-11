@api @post_echo
Feature: POST Echo Endpoint Contract Tests
  As a QA engineer
  I want to validate the POST /post echo endpoint
  So that I can ensure the API contract remains stable

  Background:
    Given the API base URL is configured

  # ──────────────────────────────────────────────────────────
  # Scenario DQ-T12 — POST form data schema validation
  # ──────────────────────────────────────────────────────────
  @contract @schema
  Scenario: Verify POST with form data returns 200 and matches schema
    When I send a POST request to "/post" with form data:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response status code should be 200
    And the response should match the POST echo JSON schema
