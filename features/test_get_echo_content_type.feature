@api @get_echo
Feature: GET Echo Endpoint Content-Type Exact Match Validation
  As a QA engineer
  I want to validate the GET /get echo endpoint returns the exact Content-Type header
  So that I can ensure the API contract for content type remains stable

  Background:
    Given the API base URL is configured

  # ──────────────────────────────────────────────────────────
  # Scenario DQ-T14 — Content-Type exact match validation
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify GET response status and exact Content-Type header
    When I send a GET request to "/get" with query parameters:
      | key | value |
      | foo | bar   |
      | baz | value |
    Then the response status code should be 200
    And the response Content-Type should equal "application/json; charset=utf-8"
