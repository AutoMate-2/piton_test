@api @post_echo
Feature: POST Echo Endpoint Form Data Echo Tests
  As a QA engineer
  I want to validate the POST /post echo endpoint echoes form data correctly
  So that I can ensure the API contract for form data remains stable

  Background:
    Given the API base URL is configured

  # ──────────────────────────────────────────────────────────
  # Scenario DQ-T10 — POST form data echo validation
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify POST with form data echoes form fields correctly
    When I send a POST request to "/post" with form data:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response status code should be 200
    And the JSON key "form" should be of type "object"
    And the JSON key "form.foo1" should equal "bar1"
    And the JSON key "form.foo2" should equal "bar2"
