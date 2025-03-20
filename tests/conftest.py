"""Configuration file for pytest."""

import os
import sys
import pytest
from sdk.base import Additel

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Define device connection details
DEFAULT_IP = "192.168.1.223"


@pytest.fixture
def device_ip():
    """Get device IP from environment or use default."""
    return os.environ.get("ADDITEL_IP", DEFAULT_IP)


@pytest.fixture
def additel(device_ip):
    """Fixture to provide an Additel connection object."""
    with Additel("wlan", ip=device_ip) as device:
        yield device


@pytest.fixture
def module_config(additel, module_index=0):
    """Fixture to provide module configuration."""
    return additel.Module.getConfiguration(module_index=module_index)


@pytest.fixture
def module_config_json(additel, module_index=0):
    """Fixture to provide module configuration in JSON format."""
    return additel.Module.getConfiguration_json(module_index=module_index)


@pytest.fixture
def scan_config(additel):
    """Fixture to provide scan configuration."""
    return additel.Scan.get_configuration()


@pytest.fixture
def scan_config_json(additel):
    """Fixture to provide scan configuration in JSON format."""
    return additel.Scan.get_configuration_json()


@pytest.fixture
def channel_config(additel, channel_name="REF1"):
    """Fixture to provide channel configuration."""
    return additel.Channel.get_configuration(channel_name)


# Helper functions
def compare_keys(a, b):
    """Helper function to compare keys between two objects."""
    for i, x in enumerate(a):
        for key in x.keys():
            assert key in b[i].keys(), f"Key {key} not found"
    for i, x in enumerate(b):
        for key in x.keys():
            assert key in a[i].keys(), f"Key {key} not found"


# Example mock in conftest.py
@pytest.fixture
def mock_additel(monkeypatch):
    """A fixture that provides a mocked Additel device."""
    from unittest.mock import MagicMock

    mock = MagicMock()
    mock.identify.return_value = "'685022040027',TAU-HOST 1.1.1.0"
    # Add other mock returns as needed
    return mock
