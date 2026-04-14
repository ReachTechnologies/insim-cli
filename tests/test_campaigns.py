"""Tests for campaigns commands."""
import pytest


def test_list_campaigns(api_client):
    """Should return campaigns."""
    result = api_client.post("/api/v2/campaigns", {"limit": 5})
    assert result["success"] is True
    assert "campaigns" in result

    if result["campaigns"]:
        camp = result["campaigns"][0]
        assert "name" in camp
        assert "message" in camp
        assert "status" in camp
        # No French keys
        assert "nom" not in camp


def test_create_and_cancel_campaign(api_client):
    """Create a draft campaign and cancel it."""
    # Create without recipients (status 2)
    result = api_client.post("/api/v2/campaigns/create", {
        "name": "Pytest Campaign",
        "message": "Test from pytest"
    })
    assert result["success"] is True
    camp = result["campaign"]
    assert camp["status"] == 2  # No recipients
    assert camp["recipients"] == 0
    camp_id = camp["id"]

    # Cancel it
    cancel = api_client.post("/api/v2/campaigns/cancel", {"campaign_id": camp_id})
    assert cancel["success"] is True
    assert cancel["cancelled"] is True


def test_create_campaign_with_phones(api_client):
    """Campaign with phone numbers should have status 0."""
    result = api_client.post("/api/v2/campaigns/create", {
        "name": "Pytest Phone Campaign",
        "message": "Test with phones",
        "phone_numbers": ["+33600000000"]
    })
    assert result["success"] is True
    assert result["campaign"]["status"] == 0
    assert result["campaign"]["recipients"] == 1

    # Cleanup
    api_client.post("/api/v2/campaigns/cancel", {"campaign_id": result["campaign"]["id"]})
