"""Create Zephyr Scale test cases from query_params.feature.

Two-step approach:
  1. POST /testcases          → create the test case
  2. PUT  /testcases/{key}/testscript → attach the BDD Gherkin script
"""

import json
import requests

ZEPHYR_BASE = "https://api.zephyrscale.smartbear.com/v2"
ZEPHYR_TOKEN = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
    "eyJjb250ZXh0Ijp7ImJhc2VVcmwiOiJodHRwczovL2F1dG9tYXRlMTIzLmF0bGFzc2lhbi5uZXQiLCJ1c2VyIjp7ImFjY291bnRJZCI6IjVmN2IzNWY0OGQ4OGIzMDA3NTIyODIyYiIsInRva2VuSWQiOiJhY2EwZGI4My03MTljLTQxMGQtOTc4My01YjZkNjI5Y2VmNGQifX0sImlzcyI6ImNvbS5rYW5vYWgudGVzdC1tYW5hZ2VyIiwic3ViIjoiNzEwNGY0MjctNmZkZC0zMzU0LWFjMTktMjliNDM4ZGVlZGUzIiwiZXhwIjoxODAyMzY5MTIyLCJpYXQiOjE3NzA4MzMxMjJ9."
    "4wqZiQBsBF3cmcCg7gmvNrWDxPZTyN41pJQEvoPqr_0"
)
PROJECT_KEY = "DQ"

HEADERS = {
    "Authorization": f"Bearer {ZEPHYR_TOKEN}",
    "Content-Type": "application/json",
}

BACKGROUND = "Given the API base URL is configured"

TEST_CASES = [
    {
        "name": "Verify response returns 200 with correct Content-Type",
        "labels": ["smoke", "positive", "query_params"],
        "script": (
            f"{BACKGROUND}\n"
            'When I send a GET request to "/get" with query parameters:\n'
            "  | key | value |\n"
            "  | foo | bar   |\n"
            "  | baz | value |\n"
            "Then the response status code should be 200\n"
            'And the response Content-Type should equal "application/json; charset=utf-8"'
        ),
    },
    {
        "name": "Verify query parameters are correctly echoed in args",
        "labels": ["contract", "positive", "query_params"],
        "script": (
            f"{BACKGROUND}\n"
            'When I send a GET request to "/get" with query parameters:\n'
            "  | key | value |\n"
            "  | foo | bar   |\n"
            "  | baz | value |\n"
            "Then the response status code should be 200\n"
            'And the JSON key "args" should be of type "object"\n'
            'And the JSON key "args.foo" should equal "bar"\n'
            'And the JSON key "args.baz" should equal "value"'
        ),
    },
    {
        "name": "Verify Date header exists and contains a valid date",
        "labels": ["contract", "headers", "query_params"],
        "script": (
            f"{BACKGROUND}\n"
            'When I send a GET request to "/get" with query parameters:\n'
            "  | key | value |\n"
            "  | foo | bar   |\n"
            "  | baz | value |\n"
            "Then the response status code should be 200\n"
            'And the response should have header "Date"\n'
            'And the response header "Date" should be a valid date'
        ),
    },
    {
        "name": "Verify response contains all required contract keys",
        "labels": ["contract", "positive", "query_params"],
        "script": (
            f"{BACKGROUND}\n"
            'When I send a GET request to "/get" with query parameters:\n'
            "  | key | value |\n"
            "  | foo | bar   |\n"
            "  | baz | value |\n"
            "Then the response should be a JSON object\n"
            'And the response JSON should contain key "args"\n'
            'And the response JSON should contain key "headers"\n'
            'And the response JSON should contain key "url"'
        ),
    },
    {
        "name": "Verify the url property contains the original request URL",
        "labels": ["contract", "positive", "query_params"],
        "script": (
            f"{BACKGROUND}\n"
            'When I send a GET request to "/get" with query parameters:\n'
            "  | key | value |\n"
            "  | foo | bar   |\n"
            "  | baz | value |\n"
            "Then the response status code should be 200\n"
            'And the JSON key "url" should contain "postman-echo.com/get"\n'
            'And the JSON key "url" should contain "foo=bar"\n'
            'And the JSON key "url" should contain "baz=value"'
        ),
    },
]


def create_test_case(tc):
    """Step 1: Create test case."""
    payload = {
        "projectKey": PROJECT_KEY,
        "name": tc["name"],
        "labels": tc["labels"],
    }
    resp = requests.post(
        f"{ZEPHYR_BASE}/testcases",
        headers=HEADERS,
        data=json.dumps(payload),
    )
    return resp


def attach_bdd_script(test_case_key, script_text):
    """Step 2: PUT the BDD Gherkin script onto the test case."""
    payload = {
        "type": "BDD",
        "text": script_text,
    }
    resp = requests.put(
        f"{ZEPHYR_BASE}/testcases/{test_case_key}/testscript",
        headers=HEADERS,
        data=json.dumps(payload),
    )
    return resp


def main():
    print(f"Creating {len(TEST_CASES)} test cases in Zephyr Scale (project {PROJECT_KEY})...\n")

    for i, tc in enumerate(TEST_CASES, 1):
        # Step 1 — Create
        resp = create_test_case(tc)
        if resp.status_code not in (200, 201):
            print(f"  [{i}/5] CREATE FAILED ({resp.status_code}) — {tc['name']}")
            print(f"           {resp.text}")
            continue

        data = resp.json()
        key = data.get("key", "N/A")
        print(f"  [{i}/5] CREATED  {key} — {tc['name']}")

        # Step 2 — Attach BDD script
        script_resp = attach_bdd_script(key, tc["script"])
        if script_resp.status_code in (200, 201):
            print(f"         BDD script attached to {key}")
        else:
            print(f"         SCRIPT FAILED ({script_resp.status_code}) — {script_resp.text}")

    print("\nDone.")


if __name__ == "__main__":
    main()
