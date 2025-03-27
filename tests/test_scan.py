"""Tests for the device SDK Scan functionality."""

import pytest
from src.additel_sdk.scan import DIScanInfo, DIReading, Scan
from typing import List, TYPE_CHECKING
from datetime import datetime
from time import sleep

if TYPE_CHECKING:
    from src.additel_sdk import Additel
from src.additel_sdk.channel import Channel


@pytest.fixture
def scan_fixture(device: "Additel") -> Scan:
    """Fixture for Scan tests."""
    return Scan(device)


def test_scan_config(scan_config: DIScanInfo, scan_config_json: DIScanInfo):
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
def test_get_scan_data_json(scan_fixture: Scan, count):
    """Test retrieval of scan data in JSON format."""
    data = scan_fixture.get_data_json(count)
    assert len(data) == 1, "Should return a list of one object"
    assert isinstance(data[0], DIReading), "Data must be a DIReading object"
    assert len(data[0].Values) == count, f"Should return {count} data points"


def test_get_latest_data(scan_fixture: Scan):
    """Test retrieval of latest scan data."""
    scan_fixture.start(DIScanInfo(1000, 'REF1'))
    sleep(0.2)
    data = scan_fixture.get_latest_data()
    print(data)
    assert isinstance(data, DIReading), "Data must be a DIReading object"


def test_scan_consistency(scan_fixture: Scan):
    """Test consistency between scan data retrieval methods."""
    # Get data using both methods
    data_json = scan_fixture.get_data_json(1)
    data_latest = scan_fixture.get_latest_data()

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


def test_intelligent_wire(scan_fixture: Scan):
    """Test intelligent wiring data retrieval."""
    intel_wire = scan_fixture.get_intelligent_wiring_data_json()
    assert isinstance(intel_wire, list), "Should return a list"


@pytest.mark.skip(reason="Will change device state in mysterious ways")
def test_get_readings(scan_fixture: Scan):
    """Test retrieval of scan readings."""
    desired_channels = Channel.valid_names
    readings = scan_fixture.get_readings(desired_channels)
    assert isinstance(readings, List), "Should return a list"
    assert all(
        isinstance(r, DIReading) for r in readings
    ), "All elements should be DIReading objects"
    for i, channel in enumerate(desired_channels):
        assert channel == readings[i].ChannelName, f"Channel {i} should be {channel}"


def test_get_configuration(scan_fixture: Scan):
    config = scan_fixture.get_configuration()
    assert isinstance(config, DIScanInfo), "Config should be a DIScanInfo object"


def test_get_configuration_json(scan_fixture: Scan):
    config = scan_fixture.get_configuration_json()
    assert isinstance(config, DIScanInfo), "Config should be a DIScanInfo object"
