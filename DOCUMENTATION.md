# Contract Testing BDD Framework — Documentation

## Table of Contents

1. [Postman Collection Overview](#1-postman-collection-overview)
2. [Project Architecture](#2-project-architecture)
3. [Design Patterns](#3-design-patterns)
4. [Module Reference](#4-module-reference)
5. [API Endpoint Catalog](#5-api-endpoint-catalog)
6. [Test Scenario Catalog](#6-test-scenario-catalog)
7. [Configuration](#7-configuration)
8. [Running Tests](#8-running-tests)
9. [Extending the Framework](#9-extending-the-framework)

---

## 1. Postman Collection Overview

**Collection:** Contract Testing
**Base URL:** `https://postman-echo.com`
**Purpose:** Validate that API contracts remain stable — response structures, status codes, headers, and echoed payloads all conform to expectations.

The collection contains **3 endpoints**:

| # | Name | Method | Path | Description |
|---|------|--------|------|-------------|
| 1 | Test Response | `GET` | `/get?foo1=bar1&foo2=bar2` | Validates response status, JSON structure, and required keys (`args`, `headers`, `url`) |
| 2 | Check for Valid Query Params | `GET` | `/get?foo=bar&baz=value` | Validates query params are echoed in `args`, Content-Type header, and Date header |
| 3 | Check for Valid Form Data | `POST` | `/post` | Validates form-data fields are echoed in `form` object |

### Collection Variable

| Variable | Value |
|----------|-------|
| `baseUrl` | `https://postman-echo.com` |

---

## 2. Project Architecture

```
piton_test/
├── config/
│   └── config.yaml                     # Environment & runtime configuration
├── core/                               # Framework core (design patterns live here)
│   ├── __init__.py
│   ├── config.py                       # Singleton — Config Manager
│   ├── api_client.py                   # Singleton — HTTP Client with connection pooling
│   ├── request_builder.py              # Builder — Fluent request construction
│   └── response_validator.py           # Fluent Interface — Chainable assertions
├── utils/                              # Shared utilities
│   ├── __init__.py
│   ├── logger.py                       # Centralized logging setup
│   └── schema_validator.py             # JSON Schema definitions for contract tests
├── features/                           # BDD layer (Behave)
│   ├── environment.py                  # Behave lifecycle hooks (setup/teardown)
│   ├── test_response.feature           # Feature file — GET /get endpoint
│   └── steps/
│       └── test_response_steps.py      # Step definitions for GET /get scenarios
├── Contract Testing.postman_collection.json  # Source Postman collection
├── behave.ini                          # Behave runner configuration
├── requirements.txt                    # Python dependencies
└── DOCUMENTATION.md                    # This file
```

### Layer Responsibilities

| Layer | Directory | Responsibility |
|-------|-----------|----------------|
| **Config** | `config/` | YAML-driven environment settings (base URL, timeouts, logging) |
| **Core** | `core/` | Reusable infrastructure: HTTP client, request building, response validation |
| **Utils** | `utils/` | Cross-cutting concerns: logging, JSON schemas |
| **Features** | `features/` | BDD scenarios, step definitions, and Behave hooks |

---

## 3. Design Patterns

### 3.1 Singleton — `Config` & `APIClient`

**Files:** `core/config.py`, `core/api_client.py`

Both classes use Python's `__new__` to guarantee a single instance throughout the test run.

**Config** loads `config/config.yaml` once and exposes properties:
```python
config = Config()
config.base_url       # "https://postman-echo.com"
config.timeout        # 30
config.endpoint("get_echo")  # "/get"
```

**APIClient** wraps `requests.Session` for connection pooling and centralized logging:
```python
client = APIClient()       # same instance everywhere
client.base_url            # reads from Config singleton
client.send(prepared_req)  # logs method, URL, status, and byte size
APIClient.reset()          # teardown: closes session, clears instance
```

### 3.2 Builder — `RequestBuilder`

**File:** `core/request_builder.py`

Fluent API that constructs HTTP requests step-by-step, then sends via the singleton client:

```python
response = (
    RequestBuilder()
    .method("GET")
    .endpoint("/get")
    .with_query_params({"foo1": "bar1", "foo2": "bar2"})
    .with_header("X-Custom", "value")
    .build()
    .send()
)
```

**Available builder methods:**

| Method | Purpose |
|--------|---------|
| `.method(str)` | HTTP verb (GET, POST, PUT, DELETE, etc.) |
| `.endpoint(str)` | Path appended to base URL |
| `.with_query_params(dict)` | URL query string parameters |
| `.with_header(key, value)` | Single header |
| `.with_headers(dict)` | Multiple headers at once |
| `.with_json_body(obj)` | JSON request body |
| `.with_form_data(dict)` | Form-encoded request body |
| `.build()` | Prepares the request, returns a sendable object |
| `.send()` | Executes the request via `APIClient.send()` |

### 3.3 Fluent Interface — `ResponseValidator`

**File:** `core/response_validator.py`

Chainable assertion methods that read like English. Every method returns `self`, enabling expressive validation chains:

```python
ResponseValidator(response) \
    .status_code(200) \
    .content_type("application/json") \
    .is_json_object() \
    .has_json_key("args") \
    .json_key_equals("args.foo1", "bar1") \
    .response_time_under(5000) \
    .matches_schema(GET_ECHO_SCHEMA)
```

**Available assertions:**

| Category | Method | Description |
|----------|--------|-------------|
| **Status** | `.status_code(int)` | Exact status code match |
| | `.status_code_in(list)` | Status in set of codes |
| **Headers** | `.content_type(str)` | Content-Type contains substring |
| | `.has_header(str)` | Header exists in response |
| | `.header_equals(name, value)` | Header exact match |
| **JSON** | `.is_json_object()` | Body is a dict |
| | `.has_json_key(path)` | Dot-path key exists (e.g. `"args.foo1"`) |
| | `.json_key_equals(path, val)` | Dot-path key equals expected value |
| | `.json_key_type(path, type)` | Dot-path key is expected Python type |
| | `.json_key_is_not_empty(path)` | Dot-path key is truthy |
| **Schema** | `.matches_schema(dict)` | Full JSON Schema validation via `jsonschema` |
| **Performance** | `.response_time_under(ms)` | Response elapsed time within threshold |

---

## 4. Module Reference

### 4.1 `core/config.py` — Config (Singleton)

| Member | Type | Description |
|--------|------|-------------|
| `base_url` | `property -> str` | API base URL from YAML |
| `timeout` | `property -> int` | Default request timeout in seconds |
| `endpoint(name)` | `method -> str` | Named endpoint path from YAML |
| `get(key, default)` | `method -> Any` | Generic config value lookup |

### 4.2 `core/api_client.py` — APIClient (Singleton)

| Member | Type | Description |
|--------|------|-------------|
| `session` | `property -> requests.Session` | Underlying session with connection pooling |
| `base_url` | `property -> str` | Delegates to `Config.base_url` |
| `send(prepared)` | `method -> Response` | Executes request with logging and timeout |
| `close()` | `method` | Closes session |
| `reset()` | `classmethod` | Closes and clears the singleton instance |

### 4.3 `core/request_builder.py` — RequestBuilder (Builder)

See [Section 3.2](#32-builder--requestbuilder) for full method listing.

### 4.4 `core/response_validator.py` — ResponseValidator (Fluent Interface)

See [Section 3.3](#33-fluent-interface--responsevalidator) for full assertion listing.

### 4.5 `utils/logger.py` — Logging Setup

Reads `logging.level` and `logging.format` from `config.yaml`. Configures a `StreamHandler` on stdout. Called once in `before_all` hook.

### 4.6 `utils/schema_validator.py` — JSON Schema Definitions

| Schema Constant | Used By | Description |
|-----------------|---------|-------------|
| `GET_ECHO_SCHEMA` | Endpoint 1 (GET /get) | Requires `args` (object), `headers` (object), `url` (string). Allows additional properties. |

### 4.7 `features/environment.py` — Behave Hooks

| Hook | Action |
|------|--------|
| `before_all` | Initializes logging, creates `APIClient` singleton |
| `after_all` | Calls `APIClient.reset()` to close connections |
| `before_scenario` | Resets `context.response` and `context.validator` to `None` |

---

## 5. API Endpoint Catalog

### Endpoint 1: Test Response

| Property | Value |
|----------|-------|
| **Name** | Test Response |
| **Method** | `GET` |
| **URL** | `https://postman-echo.com/get?foo1=bar1&foo2=bar2` |
| **Headers** | None (defaults only) |
| **Query Params** | `foo1=bar1`, `foo2=bar2` |

**Expected Response:**
```json
{
  "args": {
    "foo1": "bar1",
    "foo2": "bar2"
  },
  "headers": {
    "host": "postman-echo.com",
    "accept": "application/json",
    ...
  },
  "url": "https://postman-echo.com/get?foo1=bar1&foo2=bar2"
}
```

**Postman Tests:**
1. Status code is 200
2. Response is a JSON object
3. Response has `args` property
4. Response has `headers` property
5. Response has `url` property

**BDD Coverage:** 7 scenarios (see [Section 6](#6-test-scenario-catalog))

---

### Endpoint 2: Check for Valid Query Params

| Property | Value |
|----------|-------|
| **Name** | Check for Valid Query Params |
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/get?foo=bar&baz=value` |
| **Headers** | None (defaults only) |
| **Query Params** | `foo=bar`, `baz=value` |

**Expected Response:**
```json
{
  "args": {
    "foo": "bar",
    "baz": "value"
  },
  "headers": { ... },
  "url": "https://postman-echo.com/get?foo=bar&baz=value"
}
```

**Postman Tests:**
1. Response code is 200
2. Content-Type header equals `application/json; charset=utf-8`
3. `args` object contains correct query params (`foo` = `bar`, `baz` = `value`)
4. Date header is a valid date

**BDD Coverage:** Not yet implemented (Endpoint 1 only in current sprint)

---

### Endpoint 3: Check for Valid Form Data

| Property | Value |
|----------|-------|
| **Name** | Check for Valid Form Data |
| **Method** | `POST` |
| **URL** | `{{baseUrl}}/post` |
| **Headers** | None (auto Content-Type from form-data) |
| **Body** | form-data: `foo1=bar1`, `foo2=bar2` |

**Expected Response:**
```json
{
  "args": {},
  "data": "",
  "files": {},
  "form": {
    "foo1": "bar1",
    "foo2": "bar2"
  },
  "headers": { ... },
  "url": "https://postman-echo.com/post"
}
```

**Postman Tests:**
1. `form` object is present and contains correct form data (`foo1` = `bar1`, `foo2` = `bar2`)

**BDD Coverage:** Not yet implemented (Endpoint 1 only in current sprint)

---

## 6. Test Scenario Catalog

### Feature: GET Echo Endpoint Contract Tests

**File:** `features/test_response.feature`
**Tags:** `@api`, `@get_echo`
**Background:** Verifies base URL is configured before each scenario.

| # | Scenario | Tags | Assertions |
|---|----------|------|------------|
| 1 | Verify successful response status and content type | `@smoke` `@positive` | Status 200, Content-Type contains `application/json` |
| 2 | Verify response body contains required contract keys | `@contract` `@positive` | Body is JSON object, has keys: `args`, `headers`, `url` |
| 3 | Verify query parameters are echoed in the args object | `@contract` `@positive` | Status 200, `args.foo1` = `bar1`, `args.foo2` = `bar2` |
| 4 | Verify response matches the expected JSON schema | `@contract` `@schema` | Status 200, matches `GET_ECHO_SCHEMA` (requires `args`, `headers`, `url`) |
| 5 | Verify response time is within acceptable limits | `@performance` `@positive` | Status 200, elapsed < 5000ms |
| 6 | Verify response includes standard HTTP headers | `@contract` `@headers` | Status 200, has `Date` header, has `Content-Type` header |
| 7 | Verify GET request works with no query parameters | `@edge` `@positive` | Status 200, body is JSON object, `args` is empty `{}` |

### Step Definition Mapping

| Step Text | Function | File:Line |
|-----------|----------|-----------|
| `Given the API base URL is configured` | `step_api_base_url_configured` | `test_response_steps.py:16` |
| `When I send a GET request to "{endpoint}" with query parameters:` | `step_send_get_with_params` | `test_response_steps.py:25` |
| `When I send a GET request to "{endpoint}" without query parameters` | `step_send_get_without_params` | `test_response_steps.py:40` |
| `Then the response status code should be {status_code:d}` | `step_status_code` | `test_response_steps.py:56` |
| `And the response Content-Type should contain "{expected}"` | `step_content_type` | `test_response_steps.py:64` |
| `And the response should have header "{header_name}"` | `step_has_header` | `test_response_steps.py:69` |
| `And the response should be a JSON object` | `step_is_json_object` | `test_response_steps.py:77` |
| `And the response JSON should contain key "{key}"` | `step_has_json_key` | `test_response_steps.py:82` |
| `And the JSON key "{key_path}" should equal "{expected}"` | `step_json_key_equals` | `test_response_steps.py:87` |
| `And the JSON key "{key_path}" should be an empty object` | `step_json_key_empty_object` | `test_response_steps.py:92` |
| `And the response should match the GET echo JSON schema` | `step_matches_schema` | `test_response_steps.py:100` |
| `And the response time should be under {max_ms:d} milliseconds` | `step_response_time` | `test_response_steps.py:108` |

---

## 7. Configuration

### config/config.yaml

```yaml
base_url: "https://postman-echo.com"

endpoints:
  get_echo: "/get"

default_timeout: 30

logging:
  level: "INFO"
  format: "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
```

| Key | Type | Description |
|-----|------|-------------|
| `base_url` | string | Root URL for all API requests |
| `endpoints.<name>` | string | Named endpoint paths |
| `default_timeout` | int | HTTP request timeout in seconds |
| `logging.level` | string | Python logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `logging.format` | string | Log output format string |

### behave.ini

```ini
[behave]
paths = features
format = pretty
color = true
stdout_capture = false
stderr_capture = false
log_capture = false
```

### requirements.txt

| Package | Version | Purpose |
|---------|---------|---------|
| `behave` | 1.2.6 | BDD test runner |
| `requests` | 2.31.0 | HTTP client |
| `PyYAML` | 6.0.1 | YAML config loading |
| `jsonschema` | 4.21.1 | JSON Schema validation |

---

## 8. Running Tests

### Install Dependencies

```bash
pip3 install -r requirements.txt
```

### Run All Tests

```bash
python3 -m behave
```

### Run by Tag

```bash
python3 -m behave --tags=@smoke          # smoke tests only
python3 -m behave --tags=@contract        # contract validation
python3 -m behave --tags=@performance     # performance checks
python3 -m behave --tags=@edge            # edge cases
python3 -m behave --tags=@schema          # schema validation
python3 -m behave --tags=@headers         # header checks
python3 -m behave --tags="@contract,@smoke"  # contract OR smoke
python3 -m behave --tags="@contract and @positive"  # contract AND positive
```

### Output Formats

```bash
python3 -m behave --format pretty         # human-readable (default)
python3 -m behave --format json            # JSON output
python3 -m behave --format progress        # dots-style progress
```

---

## 9. Extending the Framework

### Adding a New Endpoint (e.g., Endpoint 2 — Valid Query Params)

**Step 1 —** Add endpoint to `config/config.yaml`:
```yaml
endpoints:
  get_echo: "/get"
  get_query_params: "/get"     # new
```

**Step 2 —** Add JSON schema to `utils/schema_validator.py` (if needed):
```python
GET_QUERY_PARAMS_SCHEMA = {
    "type": "object",
    "required": ["args", "headers", "url"],
    ...
}
```

**Step 3 —** Create feature file `features/query_params.feature`:
```gherkin
@api @query_params
Feature: Query Params Validation
  ...
```

**Step 4 —** Add any new step definitions to `features/steps/` (reuse existing steps where possible).

### Adding a POST Endpoint (e.g., Endpoint 3 — Form Data)

The `RequestBuilder` already supports `.with_form_data()`:

```python
response = (
    RequestBuilder()
    .method("POST")
    .endpoint("/post")
    .with_form_data({"foo1": "bar1", "foo2": "bar2"})
    .build()
    .send()
)
```

New step definitions for POST can reuse all existing `Then` steps — only the `When` steps need new matchers for POST-specific actions.
