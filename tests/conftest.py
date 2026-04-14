"""Test configuration and fixtures for insim-cli tests."""
import os
import pytest
from cli_anything.insim.core.api import InsimAPI

# Test credentials (real account for integration tests)
INSIM_TEST_LOGIN = "radhi1977@radhi.com"
INSIM_TEST_KEY = "zCqNiE4i1LQAbzTKpcwcXsE30hPipETgVclX3CIiIbXDPwURcp"
INSIM_TEST_BASE_URL = "https://www.insim.app"

# Test contact: douda
INSIM_TEST_CONTACT_NAME = "douda"
INSIM_TEST_CONTACT_ID = "699c64d1b2d11e1919a3efb6"
INSIM_TEST_CONTACT_PHONE = "+21696591256"

# Test message
INSIM_TEST_MESSAGE = "Je t'aime depuis CLI"


def pytest_addoption(parser):
    parser.addoption(
        "--run-integration", action="store_true", default=False,
        help="Run integration tests (sends real SMS!)"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: marks tests that send real SMS")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--run-integration"):
        skip_integration = pytest.mark.skip(reason="Need --run-integration to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)


@pytest.fixture
def api_client():
    """Return an authenticated InsimAPI client for testing."""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    return InsimAPI(INSIM_TEST_BASE_URL, INSIM_TEST_LOGIN, INSIM_TEST_KEY)
