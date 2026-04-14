"""HTTP client for inSIM API v2."""
import requests
from typing import Any


class InsimAPIError(Exception):
    """Error returned by the inSIM API."""
    def __init__(self, message: str, error_code: str = "", status: int = 0, field: str = "", extra: dict | None = None):
        self.error_code = error_code
        self.status = status
        self.field = field
        self.extra = extra or {}
        super().__init__(message)


class InsimAPI:
    """Client for inSIM API v2."""

    def __init__(self, base_url: str, login: str, access_key: str):
        self.base_url = base_url.rstrip("/")
        self.login = login
        self.access_key = access_key
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "insim-cli/1.0.0",
        })

    def post(self, endpoint: str, data: dict | None = None) -> dict:
        """POST to an API v2 endpoint with automatic auth injection."""
        payload = {
            "login": self.login,
            "accessKey": self.access_key,
        }
        if data:
            payload.update(data)

        url = f"{self.base_url}{endpoint}"

        try:
            resp = self.session.post(url, json=payload, timeout=60, verify=False)
        except requests.ConnectionError:
            raise InsimAPIError(f"Cannot connect to {self.base_url}. Is the server running?")
        except requests.Timeout:
            raise InsimAPIError("Request timed out after 30 seconds.")

        try:
            body = resp.json()
        except ValueError:
            raise InsimAPIError(f"Invalid response from server (HTTP {resp.status_code})")

        if not body.get("success", False):
            extra = {}
            if body.get("error_code") == "LICENSE_REQUIRED":
                extra = {
                    "subscription_type": body.get("subscription_type", ""),
                    "upgrade_url": body.get("upgrade_url", ""),
                    "feature": body.get("feature", ""),
                }
            raise InsimAPIError(
                message=body.get("error", "Unknown error"),
                error_code=body.get("error_code", "UNKNOWN"),
                status=resp.status_code,
                field=body.get("field", ""),
                extra=extra,
            )

        return body
