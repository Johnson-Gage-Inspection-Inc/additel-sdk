"""Tests for the base Additel SDK functionality."""

import pytest
from datetime import date
from deepdiff import DeepDiff
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.additel_sdk import Additel


def test_identify(device: "Additel"):
    """Test device identification functionality."""
    identity = device.identify()
    assert identity == {
        'Product Sequence Number': '685022040027',
        'Software Version Number': 'TAU-HOST 1.1.1.0'
        }, "Identity must be correct"


def test_connection(device: "Additel"):
    """Test that connection is properly established."""
    assert device.connection is not None, "Connection was not established"


def test_event_status_enable(device: "Additel"):
    """Test parsing of *ESE? (Event Status Enable Register)."""
    result = device.get_event_status_enable()
    assert isinstance(result, dict), "Expected a dict from get_event_status_enable"
    ok = all(isinstance(k, str) and isinstance(v, bool) for k, v in result.items())
    assert ok, "Result must be a dict of str -> bool"
    assert "Operation Complete" in result, "*ESE? result should have known status names"


def test_event_status_register(device: "Additel"):
    """Test parsing of *ESR? (Event Status Register)."""
    result = device.get_event_status_register()
    assert isinstance(result, dict), "Expected a dict from get_event_status_register"
    ok = all(isinstance(k, str) and isinstance(v, bool) for k, v in result.items())
    assert ok, "Result must be a dict of str -> bool"
    assert "Command Error" in result, "*ESR? result should contain known status names"


@pytest.mark.parametrize(
    "command,expected",
    [
        ("*ESE?", "185"),
        ("*OPC?", "1"),
        ("*IDN?", "'685022040027',TAU-HOST 1.1.1.0"),
        (
            'MODule:INFormation?',
            '0,,0,,,2,;1,6851022030037,1,TAU-M1 V01.00.00.00,TAU-M1 V01.05,20,'
            ),
        (
            'MODule:CONFig? 0',
            'REF1,1,,102,1,0,1,10,4,AM1660,1624273,291f5ef50aff4ccabb4e2a421d6fd8e0,0,0;REF2,0,,3,1,0,1,10,4,Pt100(385),,,0,0;'
            ),
        (
            'CHANnel:CONFig? "REF1"',
            'REF1,1,,102,1,0,1,10,4,AM1660,1624273,291f5ef50aff4ccabb4e2a421d6fd8e0,0,0'
        ),
        ("UNIT:TEMPerature?", "°F,1002"),
        ("DISPlay:THEMe:ALLNames?", "Dark,Light"),
        ("DISPlay:THEMe?", "Dark"),
        ("DISPlay:LANGuage?", "en-US"),
        ("SYSTem:COMMunicate:BLUEtooth:NAMe?", "Compact"),
        ("SYSTem:COMMunicate:BLUEtooth?", "0"),
        ("SYSTem:PASSword:ENABle:SENSor?", "0"),
        ("SYSTem:COMMunicate:SOCKet:ETHernet:PHYSicaladdress?", "64:33:DB:73:A9:5F"),
        ("SYSTem:COMMunicate:SOCKet:ETHernet:GATeway?", "0.0.0.0"),
        ("SYSTem:COMMunicate:SOCKet:ETHernet:MASK?", "255.255.255.0"),
        ("SYSTem:COMMunicate:SOCKet:ETHernet:ADDRess?", "192.168.0.182"),
        ("SYSTem:COMMunicate:SOCKet:ETHernet:DHCP?", "0"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:CONNect?", "Connected"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:SSID?", '"JGI Production WiFi:WEP_OFF"'),
        ("SYSTem:COMMunicate:SOCKet:WLAN:DHCP:STATe?", "1"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:DHCP?", "1"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:MAC?", "C0:EE:40:15:67:7F"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:GATeway?", "192.168.1.1"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:MASK?", "255.255.255.0"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:ADDRess?", "192.168.1.223"),
        ("SYSTem:COMMunicate:SOCKet:WLAN?", "1"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:STATe?", "1"),
        ("SYSTem:KLOCk?", "0"),
        ("SYSTem:DATE?", date.today().strftime("%Y,%m,%d")),
        (
            "MEASure:MODule:INFormation?",
            "0,,0,,,2,;1,6851022030037,1,TAU-M1 V01.00.00.00,TAU-M1 V01.05,20,",
        ),
        (
            "MODule:INFormation?",
            "0,,0,,,2,;1,6851022030037,1,TAU-M1 V01.00.00.00,TAU-M1 V01.05,20,",
        ),
    ],
)
def test_cmd(device: "Additel", command, expected):
    """Test command execution functionality."""
    response = device.cmd(command)
    diff = DeepDiff(expected, response)
    assert not diff, f"Response does not match expected: {diff}"
    assert response == expected, "Response must match expected"
