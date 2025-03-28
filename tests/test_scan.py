"""Tests for the device SDK Scan functionality."""

import pytest
from src.additel_sdk.errors import AdditelError
from src.additel_sdk.scan import DIScanInfo, DIReading, Scan
from typing import List, TYPE_CHECKING
from time import sleep
from conftest import use_wlan, use_wlan_fallback

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
    scan_fixture.start(DIScanInfo(100, 'REF1'))
    for d in scan_fixture.get_latest_data():
        assert isinstance(d, DIReading), "Data must be a DIReading object"


@pytest.mark.parametrize("input", [
        ('"REF1,1281,1,638786852530400000,109.131327,109.131327,1001,1,22.7278;"'),
        ('"CH1-01A,1243,1,638786859365600000,------,------,1001,1,------,32767,0,1001,1,23.61;"'),
        ('"REF1,1281,1,638786859365600000,109.129097,109.129097,1001,1,22.7221;CH1-01A,1243,1,638786859365600000,------,------,1001,1,------,32767,0,1001,1,23.61;"'),
        ]
    )
def test_parse_DIReading_from_str(input):
    result = DIReading.from_str(input)
    assert ";".join([str(r)[1:-2] for r in result]) == input[1:-2], "Data should match"


@pytest.mark.parametrize("input", [
        ('"REF1,1281,0,1001,0;CH1-01A,1243,0,1001,0,32767,0,1001,0;"'),
        ('"REF1,1281,0,1001,0;REF2,1281,0,1001,0;CH1-01A,1243,0,1001,0,32767,0,1001,0;CH1-01B,1243,0,1001,0,32767,0,1001,0;CH1-02A,1243,0,1001,0,32767,0,1001,0;CH1-02B,1243,0,1001,0,32767,0,1001,0;CH1-03A,1243,0,1001,0,32767,0,1001,0;CH1-03B,1243,0,1001,0,32767,0,1001,0;CH1-04A,1243,0,1001,0,32767,0,1001,0;CH1-04B,1243,0,1001,0,32767,0,1001,0;CH1-05A,1243,0,1001,0,32767,0,1001,0;CH1-05B,1243,0,1001,0,32767,0,1001,0;CH1-06A,1243,0,1001,0,32767,0,1001,0;CH1-06B,1243,0,1001,0,32767,0,1001,0;CH1-07A,1243,0,1001,0,32767,0,1001,0;CH1-07B,1243,0,1001,0,32767,0,1001,0;CH1-08A,1243,0,1001,0,32767,0,1001,0;CH1-08B,1243,0,1001,0,32767,0,1001,0;CH1-09A,1243,0,1001,0,32767,0,1001,0;CH1-09B,1243,0,1001,0,32767,0,1001,0;CH1-10A,1243,0,1001,0,32767,0,1001,0;CH1-10B,1243,0,1001,0,32767,0,1001,0;"'),
        ('"REF1,1281,1,638786933576800000,109.160738,109.160738,1001,1,22.8020;REF2,1281,1,638786930960400000,308.972246,308.972246,1001,1,585.3100;CH1-01A,1243,1,638786933600000000,------,------,1001,1,------,32767,0,1001,1,23.74;CH1-01B,1243,0,1001,0,32767,0,1001,0;CH1-02A,1243,0,1001,0,32767,0,1001,0;CH1-02B,1243,0,1001,0,32767,0,1001,0;CH1-03A,1243,0,1001,0,32767,0,1001,0;CH1-03B,1243,0,1001,0,32767,0,1001,0;CH1-04A,1243,0,1001,0,32767,0,1001,0;CH1-04B,1243,0,1001,0,32767,0,1001,0;CH1-05A,1243,0,1001,0,32767,0,1001,0;CH1-05B,1243,0,1001,0,32767,0,1001,0;CH1-06A,1243,0,1001,0,32767,0,1001,0;CH1-06B,1243,0,1001,0,32767,0,1001,0;CH1-07A,1243,0,1001,0,32767,0,1001,0;CH1-07B,1243,0,1001,0,32767,0,1001,0;CH1-08A,1243,0,1001,0,32767,0,1001,0;CH1-08B,1243,0,1001,0,32767,0,1001,0;CH1-09A,1243,0,1001,0,32767,0,1001,0;CH1-09B,1243,0,1001,0,32767,0,1001,0;CH1-10A,1243,0,1001,0,32767,0,1001,0;CH1-10B,1243,0,1001,0,32767,0,1001,0;"')
        ]
    )
def test_parse_DIReading_from_str_error(input):
    with pytest.raises(ValueError, match="No data available for this channel."):
        DIReading.from_str(input)


@pytest.mark.parametrize("desired_channels", [
    ["REF1"],
    ["REF1", "CH1-01A"],
    Channel.valid_names,
    ]
    )
def test_multi_scan_consistency(scan_fixture: Scan, desired_channels: List[str]):
    """_summary_

    Args:
        scan_fixture (Scan): _description_
    """

    pytest.mark.skipif((not use_wlan) or use_wlan_fallback,
                       reason="Must change device state to pass")
    with scan_fixture.preserve_scan_state():
        scan_fixture.start_multi_channel_scan(desired_channels, 100)
        sleep(3)
        latest_data = scan_fixture.get_latest_data()
        json_data = scan_fixture.get_data_json()
        assert len(json_data) == len(latest_data), "Data lengths should match"
        for i in range(len(json_data)):
            assert str(json_data[i]) == str(latest_data[i]), "Data should match"


def test_single_scan_consistency(scan_fixture: Scan):
    """Test consistency between scan data retrieval methods."""
    # Get data using both methods
    [data_latest] = scan_fixture.get_latest_data()
    [data_json] = scan_fixture.get_data_json(1)

    # Compare the two data objects
    assert isinstance(data_latest, DIReading), "Latest data must be a DIReading object"
    assert isinstance(data_json, DIReading), "JSON data must be a DIReading object"
    assert str(data_latest) == str(data_json), "Data should match"


def test_intelligent_wire(scan_fixture: Scan):
    """Test intelligent wiring data retrieval."""
    intel_wire = scan_fixture.get_intelligent_wiring_data_json()
    assert isinstance(intel_wire, list), "Should return a list"


def test_get_readings(scan_fixture: Scan, use_wlan, use_wlan_fallback):
    """Test retrieval of scan readings."""
    pytest.mark.skipif(use_wlan_fallback or not use_wlan,
                       reason="Must change device state to pass")
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


def test_start_command(scan_fixture: Scan):
    scan_fixture.parent.System.flush_error_queue()
    scan_info = DIScanInfo(NPLC=1000, ChannelName="REF1")
    scan_fixture.start(scan_info)
    err = scan_fixture.parent.System.get_error()
    assert err['error_code'] == 0, f"Expected no error, got {err}"


def test_start_json_command(scan_fixture: Scan):
    """Test that start_json sends the correct command with JSON configuration."""

    # Clear the error queue and status, then stop the scan
    scan_fixture.parent.System.flush_error_queue()
    scan_fixture.parent.clear_status()
    scan_fixture.stop()
    sleep(0.5)

    # Start the scan
    scan_info = DIScanInfo(NPLC=1000, ChannelName="REF2")
    scan_fixture.start_json(scan_info)
    sleep(1.5)  # or longer depending on device
    actual = scan_fixture.get_configuration()
    assert actual == scan_info, \
        AdditelError(**scan_fixture.parent.System.get_error())
