"""JSON Schema helpers for contract-level validation."""


GET_ECHO_SCHEMA = {
    "type": "object",
    "required": ["args", "headers", "url"],
    "properties": {
        "args": {"type": "object"},
        "headers": {"type": "object"},
        "url": {"type": "string", "format": "uri"},
    },
    "additionalProperties": True,
}
