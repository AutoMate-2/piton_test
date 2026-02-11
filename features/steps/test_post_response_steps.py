"""Step definitions for POST Echo endpoint contract tests."""

from behave import when, then, use_step_matcher

use_step_matcher("parse")

from core.request_builder import RequestBuilder
from core.response_validator import ResponseValidator
from utils.schema_validator import POST_ECHO_SCHEMA


# ── When ────────────────────────────────────────────────────


@when('I send a POST request to "{endpoint}" with form data:')
def step_send_post_with_form_data(context, endpoint):
    data = {row["key"]: row["value"] for row in context.table}
    response = (
        RequestBuilder()
        .method("POST")
        .endpoint(endpoint)
        .with_form_data(data)
        .build()
        .send()
    )
    context.response = response
    context.validator = ResponseValidator(response)


# ── Then — Schema ───────────────────────────────────────────


@then('the response should match the POST echo JSON schema')
def step_matches_post_schema(context):
    context.validator.matches_schema(POST_ECHO_SCHEMA)
