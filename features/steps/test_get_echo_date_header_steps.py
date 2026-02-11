"""Step definitions for GET Echo endpoint Date header validation."""

from email.utils import parsedate_to_datetime

from behave import then, use_step_matcher

use_step_matcher("parse")


# ── Then — Date Header Validation ───────────────────────────


@then('the response header "{header_name}" should be a valid date')
def step_response_header_valid_date(context, header_name):
    headers = context.response.headers
    assert header_name in headers, (
        f"Header '{header_name}' not found in response headers"
    )
    date_value = headers[header_name]
    try:
        parsed = parsedate_to_datetime(date_value)
    except Exception as e:
        raise AssertionError(
            f"Header '{header_name}' value '{date_value}' is not a valid "
            f"HTTP date: {e}"
        )
    assert parsed is not None, (
        f"Header '{header_name}' value '{date_value}' could not be parsed "
        f"as a valid date"
    )
