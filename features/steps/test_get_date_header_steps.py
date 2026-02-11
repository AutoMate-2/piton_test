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
        parsedate_to_datetime(date_value)
    except (TypeError, ValueError, IndexError) as exc:
        raise AssertionError(
            f"Header '{header_name}' value '{date_value}' is not a valid "
            f"HTTP date. Error: {exc}"
        )
