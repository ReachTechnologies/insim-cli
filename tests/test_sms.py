"""Tests for SMS commands."""
import pytest


def test_list_sms(api_client):
    """Should return SMS messages."""
    result = api_client.post("/api/v2/sms", {"limit": 3})
    assert result["success"] is True
    assert "messages" in result
    assert len(result["messages"]) <= 3

    msg = result["messages"][0]
    assert "direction" in msg
    assert msg["direction"] in ("inbound", "outbound")
    assert "phone_number" in msg
    assert "message" in msg
    # No French keys
    assert "body" not in msg
    assert "adress" not in msg
    assert "dossier" not in msg


def test_list_inbound(api_client):
    """Direction filter should work."""
    result = api_client.post("/api/v2/sms", {"direction": "inbound", "limit": 3})
    assert result["success"] is True
    for msg in result["messages"]:
        assert msg["direction"] == "inbound"


def test_sms_detail(api_client):
    """Should return full SMS detail."""
    # First get an SMS id
    listing = api_client.post("/api/v2/sms", {"limit": 1})
    if listing["messages"]:
        sms_id = listing["messages"][0]["id"]
        result = api_client.post("/api/v2/sms/detail", {"sms_id": sms_id})
        assert result["success"] is True
        assert "sms" in result
        assert result["sms"]["id"] == sms_id


def test_conversation(api_client):
    """Should return conversation in chronological order."""
    result = api_client.post("/api/v2/sms/conversation", {
        "phone_number": "+33664456336",
        "limit": 5
    })
    assert result["success"] is True
    assert result["phone_number"] == "+33664456336"
    assert "messages" in result
