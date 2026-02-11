"""Step definitions for GET Echo endpoint URL query parameter validation."""

from behave import then, use_step_matcher

use_step_matcher("parse")

from core.response_validator import ResponseValidator


# ── Then — JSON Key Contains (—————————————————————————————


@then('the JSON key "{key_path}" should contain "{substring}"')
def step_json_key_contains(context, key_path, substring):
    validator = context.validator
    json_data = validator.json
    # Resolve the key path using dot notation
    value = json_data
    for key in key_path.split("."):
        assert isinstance(value, dict), (
            f"Cannot resolve key '{key}' in path '{key_path}': "
            f"current value is {type(value).__name__}, not a dict"
        )
        assert key in value, (
            f"Key '{key}' not found in path '{key_path}'"
        )
        value = value[key]
    assert isinstance(value, str), (
        f"Expected JSON key '{key_path}' to be a string, "
        f"got {type(value).__name__}"
    )
    assert substring in value, (
        f"Expected JSON key '{key_path}' value '{value}' "
        f"to contain '{substring}'"
    )
