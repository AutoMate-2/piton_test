"""Step definitions for GET Echo endpoint exact Content-Type validation."""

from behave import then, use_step_matcher

use_step_matcher("parse")


# ── Then — Exact Content-Type ───────────────────────────────


@then('the response Content-Type should equal "{expected}"')
def step_content_type_equals(context, expected):
    actual = context.response.headers.get("Content-Type", "")
    assert actual == expected, (
        f"Expected Content-Type to equal '{expected}', "
        f"but got: '{actual}'"
    )
