@api @post_echo
Feature: POST Echo Endpoint Performance Tests
  As a QA engineer
  I want to validate the POST /post echo endpoint performance
  So that I can ensure the API responds within acceptable time limits

  Background:
    Given the API base URL is configured

  # ──────────────────────────────────────────────────────────
  # Scenario DQ-T13 — POST form data with performance check
  # ──────────────────────────────────────────────────────────
  @performance @positive
  Scenario: Verify POST with form data returns 200 within time limit
    When I send a POST request to "/post" with form data:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response status code should be 200
    And the response time should be under 5000 milliseconds
