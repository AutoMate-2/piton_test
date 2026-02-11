"""Response Validator — Fluent Interface / Chain-of-Responsibility pattern.

Provides chainable assertion methods against an HTTP response.

Usage:
    ResponseValidator(response) \
        .status_code(200) \
        .content_type("application/json") \
        .has_json_key("args") \
        .json_key_equals("args.foo1", "bar1") \
        .response_time_under(5000)
"""

from __future__ import annotations

from typing import Any

import requests


class ResponseValidator:
    def __init__(self, response: requests.Response):
        self._response = response
        self._json = None

    @property
    def response(self) -> requests.Response:
        return self._response

    @property
    def json(self) -> Any:
        if self._json is None:
            self._json = self._response.json()
        return self._json

    # ── Status ──────────────────────────────────────────────

    def status_code(self, expected: int) -> ResponseValidator:
        actual = self._response.status_code
        assert actual == expected, (
            f"Expected status {expected}, got {actual}"
        )
        return self

    def status_code_in(self, codes: list[int]) -> ResponseValidator:
        actual = self._response.status_code
        assert actual in codes, (
            f"Expected status in {codes}, got {actual}"
        )
        return self

    # ── Headers ─────────────────────────────────────────────

    def content_type(self, expected: str) -> ResponseValidator:
        actual = self._response.headers.get("Content-Type", "")
        assert expected in actual, (
            f"Expected Content-Type containing '{expected}', got '{actual}'"
        )
        return self

    def has_header(self, header_name: str) -> ResponseValidator:
        assert header_name in self._response.headers, (
            f"Header '{header_name}' not found in response"
        )
        return self

    def header_equals(self, header_name: str, expected: str) -> ResponseValidator:
        actual = self._response.headers.get(header_name)
        assert actual == expected, (
            f"Header '{header_name}': expected '{expected}', got '{actual}'"
        )
        return self

    # ── JSON Body ───────────────────────────────────────────

    def is_json_object(self) -> ResponseValidator:
        assert isinstance(self.json, dict), (
            f"Expected JSON object, got {type(self.json).__name__}"
        )
        return self

    def has_json_key(self, key_path: str) -> ResponseValidator:
        self._resolve(key_path)
        return self

    def json_key_equals(self, key_path: str, expected: Any) -> ResponseValidator:
        actual = self._resolve(key_path)
        assert actual == expected, (
            f"JSON '{key_path}': expected {expected!r}, got {actual!r}"
        )
        return self

    def json_key_type(self, key_path: str, expected_type: type) -> ResponseValidator:
        actual = self._resolve(key_path)
        assert isinstance(actual, expected_type), (
            f"JSON '{key_path}': expected type {expected_type.__name__}, "
            f"got {type(actual).__name__}"
        )
        return self

    def json_key_is_not_empty(self, key_path: str) -> ResponseValidator:
        actual = self._resolve(key_path)
        assert actual, f"JSON '{key_path}' is empty or falsy"
        return self

    # ── Performance ─────────────────────────────────────────

    def response_time_under(self, max_ms: int) -> ResponseValidator:
        elapsed_ms = self._response.elapsed.total_seconds() * 1000
        assert elapsed_ms < max_ms, (
            f"Response took {elapsed_ms:.0f}ms, limit is {max_ms}ms"
        )
        return self

    # ── Schema ──────────────────────────────────────────────

    def matches_schema(self, schema: dict) -> ResponseValidator:
        from jsonschema import validate, ValidationError
        try:
            validate(instance=self.json, schema=schema)
        except ValidationError as e:
            raise AssertionError(f"Schema validation failed: {e.message}") from e
        return self

    # ── Internal ────────────────────────────────────────────

    def _resolve(self, key_path: str) -> Any:
        """Resolve a dot-separated path like 'args.foo1' into the JSON tree."""
        keys = key_path.split(".")
        node = self.json
        for key in keys:
            if isinstance(node, dict) and key in node:
                node = node[key]
            else:
                raise AssertionError(
                    f"Key path '{key_path}' not found in response JSON "
                    f"(failed at '{key}')"
                )
        return node
