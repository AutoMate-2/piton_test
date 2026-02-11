"""API Client — Singleton pattern.

Thread-safe HTTP client wrapping requests.Session for connection pooling,
default headers, and centralized request execution.
"""

import logging
from typing import Optional

import requests

from core.config import Config

logger = logging.getLogger(__name__)


class APIClient:
    _instance: Optional["APIClient"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_session()
        return cls._instance

    def _init_session(self):
        self._config = Config()
        self._session = requests.Session()
        self._session.headers.update({
            "Accept": "application/json",
        })

    @property
    def session(self) -> requests.Session:
        return self._session

    @property
    def base_url(self) -> str:
        return self._config.base_url

    def send(self, prepared: requests.PreparedRequest) -> requests.Response:
        logger.info("%s %s", prepared.method, prepared.url)
        response = self._session.send(prepared, timeout=self._config.timeout)
        logger.info("Response: %s (%s bytes)", response.status_code, len(response.content))
        return response

    def close(self):
        self._session.close()

    @classmethod
    def reset(cls):
        if cls._instance is not None:
            cls._instance.close()
            cls._instance = None
