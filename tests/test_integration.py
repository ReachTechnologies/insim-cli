"""Integration tests — sends REAL SMS. Run with: pytest tests/ -m integration --run-integration"""
import pytest
from tests.conftest import (
    INSIM_TEST_CONTACT_ID, INSIM_TEST_CONTACT_PHONE,
    INSIM_TEST_CONTACT_NAME, INSIM_TEST_MESSAGE
)


@pytest.mark.integration
def test_search_douda(api_client):
    """Search for contact 'douda' should return results."""
    result = api_client.post("/api/v2/contacts/search", {
        "name": INSIM_TEST_CONTACT_NAME,
        "mode": "smart",
        "limit": 5
    })
    assert result["success"] is True
    assert result["count"] > 0
    # Check douda is in results
    phones = [c["phone_number"] for c in result["contacts"]]
    assert INSIM_TEST_CONTACT_PHONE in phones


@pytest.mark.integration
def test_send_sms_to_douda(api_client):
    """Send a real SMS to douda: 'Je t'aime depuis CLI'."""
    result = api_client.post("/api/v2/sendsms", {
        "messages": [{
            "phone_number": INSIM_TEST_CONTACT_PHONE,
            "message": INSIM_TEST_MESSAGE,
            "url": "",
            "priority": 1
        }]
    })
    assert result["success"] is True
    assert result["sent_count"] == 1


@pytest.mark.integration
def test_campaign_sms_to_douda(api_client):
    """Create and start a campaign to douda: 'Je t'aime depuis CLI'."""

    # Step 1: Create a list
    list_result = api_client.post("/api/v2/lists/create", {
        "name": "CLI Integration Test",
        "description": "Test campaign from pytest"
    })
    assert list_result["success"] is True
    list_id = list_result["list"]["id"]

    try:
        # Step 2: Add douda to the list
        add_result = api_client.post("/api/v2/lists/contacts/add", {
            "list_id": list_id,
            "contact_ids": [INSIM_TEST_CONTACT_ID]
        })
        assert add_result["success"] is True
        assert add_result["added"] == 1

        # Step 3: Create campaign
        camp_result = api_client.post("/api/v2/campaigns/create", {
            "name": "CLI Love Campaign",
            "message": INSIM_TEST_MESSAGE,
            "list_id": list_id
        })
        assert camp_result["success"] is True
        assert camp_result["campaign"]["status"] == 0  # Has recipients
        assert camp_result["campaign"]["recipients"] == 1
        camp_id = camp_result["campaign"]["id"]

        # Step 4: Start campaign
        start_result = api_client.post("/api/v2/campaigns/start", {
            "campaign_id": camp_id
        })
        assert start_result["success"] is True

    finally:
        # Cleanup: delete list (campaign may already be launched)
        api_client.post("/api/v2/lists/delete", {"list_id": list_id})
