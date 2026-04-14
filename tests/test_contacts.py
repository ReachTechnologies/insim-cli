"""Tests for contacts commands."""
import pytest
from cli_anything.insim.core.api import InsimAPIError


def test_list_contacts(api_client):
    """Should return contacts with pagination."""
    result = api_client.post("/api/v2/contacts", {"limit": 3})
    assert result["success"] is True
    assert "contacts" in result
    assert len(result["contacts"]) <= 3
    assert result["total"] > 0
    assert "has_more" in result

    # Check fields are in English
    contact = result["contacts"][0]
    assert "lastname" in contact
    assert "firstname" in contact
    assert "phone_number" in contact
    # French fields should NOT appear
    assert "nom_contact" not in contact
    assert "prenom_contact" not in contact


def test_search_contact_by_name(api_client):
    """Smart search should find 'mourad'."""
    result = api_client.post("/api/v2/contacts/search", {
        "name": "mourad",
        "mode": "smart",
        "limit": 5
    })
    assert result["success"] is True
    assert result["count"] > 0
    top = result["contacts"][0]
    assert top["score"] > 0
    assert "mourad" in top["lastname"].lower() or "mourad" in top.get("firstname", "").lower()


def test_search_contact_fuzzy(api_client):
    """Partial search 'moura' should find mourad."""
    result = api_client.post("/api/v2/contacts/search", {
        "name": "moura",
        "mode": "starts_with",
        "limit": 5
    })
    assert result["success"] is True
    assert result["count"] > 0


def test_find_by_phone(api_client):
    """Find contact by phone number."""
    result = api_client.post("/api/v2/find_contact", {
        "phone_number": "+33664456336"
    })
    assert result["success"] is True
    assert result["count"] > 0
    assert result["contacts"][0]["phone_number"] == "+33664456336"


def test_contact_detail(api_client):
    """Should return full contact in English."""
    result = api_client.post("/api/v2/contacts/detail", {
        "id_contact": "699c64ceb2d11e1919a3eb9a"
    })
    assert result["success"] is True
    contact = result["contact"]
    assert "lastname" in contact
    assert "phone_number" in contact
    assert "tags" in contact
    assert "pro" in contact
    assert isinstance(contact["pro"], bool)


def test_tags_add_remove(api_client):
    """Add and remove a tag."""
    cid = "699c64ceb2d11e1919a3eb9a"

    # Add
    result = api_client.post("/api/v2/contacts/tags", {
        "id_contact": cid,
        "add": ["pytest_tag"],
        "remove": []
    })
    assert result["success"] is True
    assert "pytest_tag" in result["tags"]

    # Remove
    result2 = api_client.post("/api/v2/contacts/tags", {
        "id_contact": cid,
        "add": [],
        "remove": ["pytest_tag"]
    })
    assert result2["success"] is True
    assert "pytest_tag" not in result2["tags"]
