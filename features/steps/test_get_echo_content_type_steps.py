"""Step definitions for GET Echo endpoint Content-Type exact match validation."""

from behave import then, use_step_matcher

use_step_matcher("parse")


# ── Then — Content-Type Exact Match ─────────────────────────


@then('the response Content-Type should equal "{expected}"')
def step_content_type_equals(context, expected):
    actual = context.response.headers.get("Content-Type", "")
    assert actual == expected, (
        f"Expected Content-Type to equal '{expected}', got '{actual}'"
    )
