@api @get_echo
Feature: GET Echo Endpoint Args Type and Value Validation
  As a QA engineer
  I want to validate the GET /get echo endpoint args type and echoed values
  So that I can ensure query parameters are correctly typed and echoed back

  Background:
    Given the API base URL is configured

  # ──────────────────────────────────────────────────────────
  # Scenario DQ-T15 — Args type and query param echo validation
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify GET response args is an object with echoed query parameters
    When I send a GET request to "/get" with query parameters:
      | key | value |
      | foo | bar   |
      | baz | value |
    Then the response status code should be 200
    And the JSON key "args" should be of type "object"
    And the JSON key "args.foo" should equal "bar"
    And the JSON key "args.baz" should equal "value"
