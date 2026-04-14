"""Tests for calls commands."""
import pytest


def test_list_calls(api_client):
    """Should return call log."""
    result = api_client.post("/api/v2/calls", {"limit": 3})
    assert result["success"] is True
    assert "calls" in result

    if result["calls"]:
        call = result["calls"][0]
        assert "type" in call
        assert "phone_number" in call
        assert "duration" in call
        assert "duration_seconds" in call
        # No French keys
        assert "typecall" not in call
        assert "adress" not in call
        assert "callduration" not in call


def test_list_outgoing(api_client):
    """Type filter should work."""
    result = api_client.post("/api/v2/calls", {"type": "outgoing", "limit": 3})
    assert result["success"] is True
    for call in result["calls"]:
        assert call["type"] == "outgoing"


def test_qualification_options(api_client):
    """Should return qualification options list."""
    result = api_client.post("/api/v2/qualifications/options")
    assert result["success"] is True
    assert "options" in result
