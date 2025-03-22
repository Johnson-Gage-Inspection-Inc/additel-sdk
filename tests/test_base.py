"""Tests for the base Additel SDK functionality."""

import pytest


def test_identify(device):
    """Test device identification functionality."""
    identity = device.identify()
    assert identity == "'685022040027',TAU-HOST 1.1.1.0", "Identity must be correct"


def test_connection(device):
    """Test that connection is properly established."""
    assert device.connection.connection is not None, "Connection was not established"


@pytest.mark.parametrize(
    "command,expected_contains",
    [
        ("*IDN?", "TAU-HOST"),
    ],
)
def test_cmd(device, command, expected_contains):
    """Test command execution functionality."""
    response = device.cmd(command)
    assert (
        expected_contains in response
    ), f"Response should contain '{expected_contains}'"
