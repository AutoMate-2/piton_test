"""Request Builder — Builder pattern.

Fluent API to construct HTTP requests step-by-step before sending.

Usage:
    response = (
        RequestBuilder()
        .method("GET")
        .endpoint("/get")
        .with_query_params({"foo1": "bar1"})
        .with_header("X-Custom", "value")
        .build()
        .send()
    )
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from core.api_client import APIClient


class RequestBuilder:
    def __init__(self):
        self._client = APIClient()
        self._method: str = "GET"
        self._path: str = "/"
        self._params: Optional[Dict[str, str]] = None
        self._headers: Dict[str, str] = {}
        self._body: Optional[Any] = None
        self._content_type: Optional[str] = None

    def method(self, http_method: str) -> RequestBuilder:
        self._method = http_method.upper()
        return self

    def endpoint(self, path: str) -> RequestBuilder:
        self._path = path
        return self

    def with_query_params(self, params: Dict[str, str]) -> RequestBuilder:
        self._params = params
        return self

    def with_header(self, key: str, value: str) -> RequestBuilder:
        self._headers[key] = value
        return self

    def with_headers(self, headers: Dict[str, str]) -> RequestBuilder:
        self._headers.update(headers)
        return self

    def with_json_body(self, body: Any) -> RequestBuilder:
        self._body = body
        self._content_type = "application/json"
        return self

    def with_form_data(self, data: Dict[str, str]) -> RequestBuilder:
        self._body = data
        self._content_type = "application/x-www-form-urlencoded"
        return self

    def build(self) -> _PreparedSendable:
        url = f"{self._client.base_url}{self._path}"
        req = requests.Request(
            method=self._method,
            url=url,
            headers=self._headers,
            params=self._params,
        )
        if self._content_type == "application/json":
            req.json = self._body
        elif self._body is not None:
            req.data = self._body

        prepared = self._client.session.prepare_request(req)
        return _PreparedSendable(prepared, self._client)


class _PreparedSendable:
    """Thin wrapper that exposes .send() on a prepared request."""

    def __init__(self, prepared: requests.PreparedRequest, client: APIClient):
        self._prepared = prepared
        self._client = client

    def send(self) -> requests.Response:
        return self._client.send(self._prepared)
