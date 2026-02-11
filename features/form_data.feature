@api @form_data
Feature: Valid Form Data Contract Tests
  As a QA engineer
  I want to validate the POST /post endpoint echoes form data correctly
  So that I can ensure form-data handling remains stable

  Background:
    Given the API base URL is configured

  # ──────────────────────────────────────────────────────────
  # Scenario 1 — Status code and JSON response
  # ──────────────────────────────────────────────────────────
  @smoke @positive
  Scenario: Verify POST returns 200 with JSON content type
    When I send a POST request to "/post" with form data:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response status code should be 200
    And the response Content-Type should contain "application/json"
    And the response should be a JSON object

  # ──────────────────────────────────────────────────────────
  # Scenario 2 — Form data echoed back in form object
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify form data fields are echoed in the form object
    When I send a POST request to "/post" with form data:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response status code should be 200
    And the JSON key "form" should be of type "object"
    And the JSON key "form.foo1" should equal "bar1"
    And the JSON key "form.foo2" should equal "bar2"

  # ──────────────────────────────────────────────────────────
  # Scenario 3 — Response body contract structure
  # ──────────────────────────────────────────────────────────
  @contract @positive
  Scenario: Verify response contains all required contract keys
    When I send a POST request to "/post" with form data:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response should be a JSON object
    And the response JSON should contain key "form"
    And the response JSON should contain key "headers"
    And the response JSON should contain key "url"

  # ──────────────────────────────────────────────────────────
  # Scenario 4 — JSON schema validation
  # ──────────────────────────────────────────────────────────
  @contract @schema
  Scenario: Verify response matches the POST echo JSON schema
    When I send a POST request to "/post" with form data:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response status code should be 200
    And the response should match the POST echo JSON schema

  # ──────────────────────────────────────────────────────────
  # Scenario 5 — Performance: response time under threshold
  # ──────────────────────────────────────────────────────────
  @performance @positive
  Scenario: Verify response time is within acceptable limits
    When I send a POST request to "/post" with form data:
      | key  | value |
      | foo1 | bar1  |
      | foo2 | bar2  |
    Then the response status code should be 200
    And the response time should be under 5000 milliseconds
