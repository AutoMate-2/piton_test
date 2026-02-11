"""Step definitions for GET Echo endpoint contract tests."""

from behave import given, when, then, use_step_matcher

use_step_matcher("parse")

from core.config import Config
from core.request_builder import RequestBuilder
from core.response_validator import ResponseValidator
from utils.schema_validator import GET_ECHO_SCHEMA


# ── Given ───────────────────────────────────────────────────


@given('the API base URL is configured')
def step_api_base_url_configured(context):
    config = Config()
    assert config.base_url, "Base URL is not configured"


# ── When ────────────────────────────────────────────────────


@when('I send a GET request to "{endpoint}" with query parameters:')
def step_send_get_with_params(context, endpoint):
    params = {row["key"]: row["value"] for row in context.table}
    response = (
        RequestBuilder()
        .method("GET")
        .endpoint(endpoint)
        .with_query_params(params)
        .build()
        .send()
    )
    context.response = response
    context.validator = ResponseValidator(response)


@when('I send a GET request to "{endpoint}" without query parameters')
def step_send_get_without_params(context, endpoint):
    response = (
        RequestBuilder()
        .method("GET")
        .endpoint(endpoint)
        .build()
        .send()
    )
    context.response = response
    context.validator = ResponseValidator(response)


# ── Then — Status ───────────────────────────────────────────


@then('the response status code should be {status_code:d}')
def step_status_code(context, status_code):
    context.validator.status_code(status_code)


# ── Then — Headers ──────────────────────────────────────────


@then('the response Content-Type should contain "{expected}"')
def step_content_type(context, expected):
    context.validator.content_type(expected)


@then('the response should have header "{header_name}"')
def step_has_header(context, header_name):
    context.validator.has_header(header_name)


# ── Then — JSON Structure ───────────────────────────────────


@then('the response should be a JSON object')
def step_is_json_object(context):
    context.validator.is_json_object()


@then('the response JSON should contain key "{key}"')
def step_has_json_key(context, key):
    context.validator.has_json_key(key)


@then('the JSON key "{key_path}" should equal "{expected}"')
def step_json_key_equals(context, key_path, expected):
    context.validator.json_key_equals(key_path, expected)


@then('the JSON key "{key_path}" should be an empty object')
def step_json_key_empty_object(context, key_path):
    context.validator.json_key_equals(key_path, {})


# ── Then — Schema ───────────────────────────────────────────


@then('the response should match the GET echo JSON schema')
def step_matches_schema(context):
    context.validator.matches_schema(GET_ECHO_SCHEMA)


# ── Then — Performance ──────────────────────────────────────


@then('the response time should be under {max_ms:d} milliseconds')
def step_response_time(context, max_ms):
    context.validator.response_time_under(max_ms)
