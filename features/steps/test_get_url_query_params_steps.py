"""Step definitions for GET Echo endpoint URL query parameter validation."""

from behave import then, use_step_matcher

use_step_matcher("parse")


# ── Then — JSON Key Contains ────────────────────────────────


@then('the JSON key "{key_path}" should contain "{expected_substring}"')
def step_json_key_contains(context, key_path, expected_substring):
    value = context.validator.json
    for part in key_path.split("."):
        assert isinstance(value, dict), (
            f"Cannot resolve key path '{key_path}': "
            f"expected dict but got {type(value).__name__}"
        )
        assert part in value, (
            f"Key '{part}' not found in JSON at path '{key_path}'"
        )
        value = value[part]
    assert isinstance(value, str), (
        f"Expected value at '{key_path}' to be a string, "
        f"but got {type(value).__name__}: {value!r}"
    )
    assert expected_substring in value, (
        f"Expected '{key_path}' value to contain '{expected_substring}', "
        f"but got: '{value}'"
    )
