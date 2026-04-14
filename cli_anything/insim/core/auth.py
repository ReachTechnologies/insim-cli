"""Authentication: login, logout, credentials storage."""
import json
import os
from pathlib import Path
from typing import Optional
from cli_anything.insim.core.api import InsimAPI, InsimAPIError

CREDENTIALS_DIR = Path.home() / ".insim"
CREDENTIALS_FILE = CREDENTIALS_DIR / "credentials.json"
DEFAULT_BASE_URL = "https://www.insim.app"


def get_base_url() -> str:
    return os.environ.get("INSIM_BASE_URL", DEFAULT_BASE_URL)


def save_credentials(login: str, access_key: str, base_url: str = "") -> None:
    CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
    data = {"login": login, "accessKey": access_key}
    if base_url:
        data["base_url"] = base_url
    CREDENTIALS_FILE.write_text(json.dumps(data, indent=2))


def load_credentials() -> Optional[dict]:
    # Priority 1: environment variables
    env_login = os.environ.get("INSIM_LOGIN")
    env_key = os.environ.get("INSIM_ACCESS_KEY")
    if env_login and env_key:
        return {"login": env_login, "accessKey": env_key}

    # Priority 2: credentials file
    if CREDENTIALS_FILE.exists():
        try:
            return json.loads(CREDENTIALS_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            return None

    return None


def remove_credentials() -> bool:
    if CREDENTIALS_FILE.exists():
        CREDENTIALS_FILE.unlink()
        return True
    return False


def login(email: str, access_key: str) -> dict:
    """Validate credentials against the API and save them."""
    base_url = get_base_url()
    api = InsimAPI(base_url, email, access_key)
    result = api.post("/api/v2/account")
    save_credentials(email, access_key, base_url)
    return result.get("account", {})


def require_auth() -> InsimAPI:
    """Return an authenticated API client or raise an error."""
    creds = load_credentials()
    if not creds:
        raise InsimAPIError(
            "Not logged in. Run: insim login YOUR_EMAIL --key YOUR_ACCESS_KEY",
            error_code="NOT_AUTHENTICATED",
        )
    base_url = creds.get("base_url", get_base_url())
    return InsimAPI(base_url, creds["login"], creds["accessKey"])


def whoami() -> dict:
    """Return account info for the current user."""
    api = require_auth()
    result = api.post("/api/v2/account")
    return result.get("account", {})
