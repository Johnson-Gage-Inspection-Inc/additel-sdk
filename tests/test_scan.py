"""Tests for the Additel SDK Scan functionality."""

import pytest
from src.additel_sdk.scan import DIScanInfo, DIReading, DITemperatureReading


def test_scan_config(additel, scan_config, scan_config_json):
    """Test scan configuration consistency."""
    assert isinstance(
        scan_config, DIScanInfo
    ), "Scan config must be a DIScanInfo object"
    assert isinstance(
        scan_config_json, DIScanInfo
    ), "JSON scan config must be a DIScanInfo object"
    assert str(scan_config_json) == str(
        scan_config
    ), "Configs should convert to same string"
    assert scan_config_json == scan_config, "Configs should be equal"


@pytest.mark.parametrize("count", [1, 2])
def test_get_scan_data_json(additel, count):
    """Test retrieval of scan data in JSON format."""
    data = additel.Scan.get_data_json(count)
    assert len(data.Values) == count, f"Should return {count} data points"
    assert isinstance(data, DITemperatureReading), "Data must be a DIReading object"


def test_get_latest_data(additel):
    """Test retrieval of latest scan data."""
    data = additel.Scan.get_latest_data()
    assert isinstance(data, DIReading), "Data must be a DIReading object"


def test_scan_consistency(additel):
    """Test consistency between scan data retrieval methods."""
    # Get data using both methods
    data_json = additel.Scan.get_data_json(1)
    data_latest = additel.Scan.get_latest_data()

    # We can't compare directly due to timestamp differences, but we can check structure
    assert len(data_latest.Values) > 0, "Latest data should not be empty"
    assert len(data_json.Values) > 0, "Data from JSON should not be empty"

    # Check same channel is reported
    assert (
        data_json.ChannelName == data_latest.ChannelName
    ), "Channel names should match"


def test_intelligent_wire(additel):
    """Test intelligent wiring data retrieval."""
    intel_wire = additel.Scan.get_intelligent_wiring_data_json()
    assert isinstance(intel_wire, list), "Should return a list"
