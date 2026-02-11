"""Configuration Manager — Singleton pattern.

Loads YAML config once and provides global access.
"""

import os
import yaml


class Config:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load()
        return cls._instance

    @classmethod
    def _load(cls):
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "config", "config.yaml"
        )
        with open(config_path, "r") as f:
            cls._config = yaml.safe_load(f)

    @property
    def base_url(self) -> str:
        return self._config["base_url"]

    @property
    def timeout(self) -> int:
        return self._config.get("default_timeout", 30)

    def endpoint(self, name: str) -> str:
        return self._config["endpoints"][name]

    def get(self, key: str, default=None):
        return self._config.get(key, default)
