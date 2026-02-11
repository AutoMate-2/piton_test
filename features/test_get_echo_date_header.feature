@api @get_echo
Feature: GET Echo Endpoint Date Header Validation
  As a QA engineer
  I want to validate the GET /get echo endpoint returns a valid Date header
  So that I can ensure the API returns properly formatted HTTP date headers

  Background:
    Given the API base URL is configured

  # ──────────────────────────────────────────────────────────
  # Scenario DQ-T16 — Date header is present and valid
  # ──────────────────────────────────────────────────────────
  @contract @headers
  Scenario: Verify GET response includes a valid Date header
    When I send a GET request to "/get" with query parameters:
      | key | value |
      | foo | bar   |
      | baz | value |
    Then the response status code should be 200
    And the response should have header "Date"
    And the response header "Date" should be a valid date
