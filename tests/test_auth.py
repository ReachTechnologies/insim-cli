"""Tests for authentication module."""
import json
import os
import tempfile
import pytest
from cli_anything.insim.core.api import InsimAPI, InsimAPIError
from cli_anything.insim.core import auth
from tests.conftest import INSIM_TEST_LOGIN, INSIM_TEST_KEY, INSIM_TEST_BASE_URL


def test_login_valid(api_client):
    """Valid credentials should return account info."""
    result = api_client.post("/api/v2/account")
    assert result["success"] is True
    assert "account" in result
    assert result["account"]["login"] == INSIM_TEST_LOGIN


def test_login_invalid():
    """Invalid credentials should raise InsimAPIError."""
    import urllib3
    urllib3.disable_warnings()
    api = InsimAPI(INSIM_TEST_BASE_URL, INSIM_TEST_LOGIN, "wrong_key")
    with pytest.raises(InsimAPIError) as exc:
        api.post("/api/v2/account")
    assert exc.value.error_code == "INVALID_CREDENTIALS"


def test_credentials_file():
    """Credentials should be saved and loaded from file."""
    from pathlib import Path
    original_file = auth.CREDENTIALS_FILE
    original_dir = auth.CREDENTIALS_DIR
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            auth.CREDENTIALS_DIR = Path(tmpdir)
            auth.CREDENTIALS_FILE = Path(tmpdir) / "creds.json"

            auth.save_credentials("test@test.com", "testkey123")

            creds = auth.load_credentials()
            assert creds is not None
            assert creds["login"] == "test@test.com"
            assert creds["accessKey"] == "testkey123"
    finally:
        auth.CREDENTIALS_FILE = original_file
        auth.CREDENTIALS_DIR = original_dir


def test_env_vars_priority(monkeypatch):
    """Environment variables should take priority over file."""
    monkeypatch.setenv("INSIM_LOGIN", "env@test.com")
    monkeypatch.setenv("INSIM_ACCESS_KEY", "envkey")

    creds = auth.load_credentials()
    assert creds is not None
    assert creds["login"] == "env@test.com"
    assert creds["accessKey"] == "envkey"


def test_whoami(api_client):
    """whoami should return account info."""
    result = api_client.post("/api/v2/account")
    account = result["account"]
    assert "login" in account
    assert "sms_credits" in account
    assert "active" in account
