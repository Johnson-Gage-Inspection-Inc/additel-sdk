"""Configuration file for pytest."""

import os
import sys
import pytest
from src.additel_sdk import Additel
from src.additel_sdk.channel import Channel, DIFunctionChannelConfig
from src.additel_sdk.module import Module
from src.additel_sdk.scan import Scan, DIScanInfo
from typing import List

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Define device connection details
DEFAULT_IP = "192.168.1.223"


@pytest.fixture
def device_ip():
    """Get device IP from environment or use default."""
    return os.environ.get("ADDITEL_IP", DEFAULT_IP)


@pytest.fixture
def module_config(device, module_index=0) -> List[DIFunctionChannelConfig]:
    """Fixture to provide module configuration."""
    mod = Module(device)
    return mod.getConfiguration(module_index=module_index)


@pytest.fixture
def module_config_json(device, module_index=0) -> List[DIFunctionChannelConfig]:
    """Fixture to provide module configuration in JSON format."""
    mod = Module(device)
    return mod.getConfiguration_json(module_index=module_index)


@pytest.fixture
def scan_config(device) -> DIScanInfo:
    """Fixture to provide scan configuration."""
    scan = Scan(device)
    return scan.get_configuration()


@pytest.fixture
def scan_config_json(device):
    """Fixture to provide scan configuration in JSON format."""
    scan = Scan(device)
    return scan.get_configuration_json()


@pytest.fixture
def channel_config(device, channel_name="REF1"):
    """Fixture to provide channel configuration."""
    chan = Channel(device)
    return chan.configure(channel_name)


# Helper functions
def compare_keys(a, b):
    """Helper function to compare keys between two objects."""
    for i, x in enumerate(a):
        for key in x.__dict__.keys():
            assert key in b[i].__dict__.keys(), f"Key {key} not found"
    for i, x in enumerate(b):
        for key in x.__dict__.keys():
            assert key in a[i].__dict__.keys(), f"Key {key} not found"


def pytest_addoption(parser):
    parser.addoption(
        "--real",
        action="store_true",
        default=False,
        help="Use real Additel device instead of mock",
    )
    parser.addoption(
        "--wlan_fallback",
        action="store_true",
        default=False,
        help="Use WLAN fallback in mock connection",
    )


@pytest.fixture
def device(request: pytest.FixtureRequest, device_ip):
    """Fixture that provides an Additel device - 
    either real or mock based on the --real flag.
    """
    
    if request.config.getoption("--real"):
        # Use real connection
        with Additel("wlan", ip=device_ip) as real_device:
            yield real_device
    else:
        # Use mock connection
        response_file = os.path.join(os.path.dirname(__file__), 'mockADT286.json')
        # Pass the device_ip to MockConnection
        use_wlan_fallback = request.config.getoption("--wlan_fallback")
        with Additel("mock",
                     response_file=response_file,
                     ip=device_ip,
                     use_wlan_fallback=use_wlan_fallback
                     ) as mock_device:
            yield mock_device