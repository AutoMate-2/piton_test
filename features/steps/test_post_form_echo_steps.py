"""Step definitions for POST Echo endpoint form data echo tests (DQ-T10)."""

from behave import then, use_step_matcher

use_step_matcher("parse")


# ── Then — JSON Type ────────────────────────────────────────


@then('the JSON key "{key_path}" should be of type "{expected_type}"')
def step_json_key_type(context, key_path, expected_type):
    type_map = {
        "object": dict,
        "array": list,
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
    }
    python_type = type_map.get(expected_type)
    assert python_type is not None, f"Unknown type name: {expected_type}"
    context.validator.json_key_type(key_path, python_type)
