"""Step definitions for POST form data contract tests (new steps only)."""

from behave import then, use_step_matcher

use_step_matcher("parse")


# ── Then — JSON Type ────────────────────────────────────────


@then('the JSON key "{key_path}" should be of type "{expected_type}"')
def step_json_key_type(context, key_path, expected_type):
    type_map = {
        "object": dict,
        "array": list,
        "string": str,
        "number": (int, float),
        "integer": int,
        "boolean": bool,
    }
    python_type = type_map.get(expected_type)
    assert python_type is not None, (
        f"Unknown type '{expected_type}'. "
        f"Supported types: {list(type_map.keys())}"
    )
    context.validator.json_key_type(key_path, python_type)
