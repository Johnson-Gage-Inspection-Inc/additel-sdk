"""Tests for the device SDK Scan functionality."""

import pytest
from src.additel_sdk.scan import DIScanInfo, DIReading, Scan
from datetime import datetime


def test_scan_config(device, scan_config: DIScanInfo, scan_config_json: DIScanInfo):
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
def test_get_scan_data_json(device, count):
    """Test retrieval of scan data in JSON format."""
    scan = Scan(device)
    data = scan.get_data_json(count)
    assert len(data.Values) == count, f"Should return {count} data points"
    assert isinstance(data, DIReading), "Data must be a DIReading object"


def test_get_latest_data(device):
    """Test retrieval of latest scan data."""
    scan = Scan(device)
    data = scan.get_latest_data()
    print(data)
    assert isinstance(data, DIReading), "Data must be a DIReading object"


def test_scan_consistency(device):
    """Test consistency between scan data retrieval methods."""
    # Get data using both methods
    scan = Scan(device)
    data_json = scan.get_data_json(1)
    data_latest = scan.get_latest_data()

    # Compare the two data objects
    assert isinstance(data_latest, DIReading), "Latest data must be a DIReading object"
    assert isinstance(data_json, DIReading), "JSON data must be a DIReading object"
    for k in data_latest.__dict__.keys():
        if getattr(data_latest, k) == getattr(data_json, k):
            continue
        elif isinstance(getattr(data_latest, k), list) and isinstance(
            getattr(data_json, k), list
        ):
            for i in range(len(getattr(data_latest, k))):
                if getattr(data_latest, k)[i] == getattr(data_json, k)[i]:
                    continue
                # assert that getattr(data_latest, k)[i] and getattr(data_json, k)[i] are the same type
                assert isinstance(
                    getattr(data_latest, k)[i], type(getattr(data_json, k)[i])
                ), "List values should be the same type"
                type_ = type(getattr(data_latest, k)[i])
                if type_ is float:
                    assert (
                        abs(getattr(data_latest, k)[i] - getattr(data_json, k)[i])
                        < 0.01
                    ), "List values should be close"
                elif type_ is datetime:
                    assert (
                        getattr(data_latest, k)[i] - getattr(data_json, k)[i]
                    ).total_seconds() < 3, "List values should be close"
            continue
        raise ValueError(f"Key {k} values do not match between data objects")


def test_intelligent_wire(device):
    """Test intelligent wiring data retrieval."""
    scan = Scan(device)
    intel_wire = scan.get_intelligent_wiring_data_json()
    assert isinstance(intel_wire, list), "Should return a list"
