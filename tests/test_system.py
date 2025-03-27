"""Tests for the Additel SDK System functionality using a dummy parent."""

import pytest
from datetime import date
from src.additel_sdk.system import System
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.additel_sdk import Additel


@pytest.fixture
def system(device):
    return System(device)


def test_get_version_no_module(system: System, device: "Additel"):
    result = system.get_version()
    expected = '1999.0'
    assert result == expected
    assert device.command_log[-1] == "SYSTem:VERSion?"


def test_get_version_with_module(system: System, device: "Additel"):
    result = system.get_version("APPLication")
    expected = {"Application": "v1.2"}
    assert result == expected
    assert device.command_log[-1] == "SYSTem:VERSion? APPLication"


def test_get_error(system: System, device: "Additel"):
    result = system.get_error()
    error_code = result.get('error_code')
    error_message = result.get('error_message')
    assert error_code is not None, "Error code not found in response."
    assert error_message is not None, "Error message not found in response."
    assert device.command_log[-1] == "SYSTem:ERRor?"
    print(result)
    pass


def test_get_error_next(system: System, device: "Additel"):
    result = system.get_error(next=True)
    error_code = result.get('error_code')
    error_message = result.get('error_message')
    assert error_code is not None, "Error code not found in response."
    assert error_message is not None, "Error message not found in response."
    assert device.command_log[-1] == "SYSTem:ERRor:NEXT?"
    print(result)
    pass


def test_set_date(system: System, device: "Additel"):
    if device.connection.type == "wlan":
        pytest.skip(reason="Would change device date.")
    system.set_date(2025, 3, 26)
    expected = "SYSTem:DATE 2025,3,26"
    assert device.command_log[-1] == expected


def test_get_date(system: System, device: "Additel"):
    result = system.get_date()
    expected = date.today()
    assert result == expected
    assert device.command_log[-1] == "SYSTem:DATE?"


def test_set_time(system: System, device: "Additel"):
    if device.connection.type == "wlan":
        pytest.skip(reason="Would change device time.")
    system.set_time(12, 34, 56)
    expected = "SYSTem:TIME 12,34,56"
    assert device.command_log[-1] == expected


@pytest.mark.parametrize(
    "lock_value,expected",
    [
        (True, "SYSTem:KLOCk 1"),
        (False, "SYSTem:KLOCk 0")
    ]
)
def test_set_local_lock(system: System, device: "Additel", lock_value, expected):
    if device.connection.type == "wlan":
        pytest.skip(reason="Would change device state.")
    system.set_local_lock(lock_value)
    assert device.command_log[-1] == expected


@pytest.mark.parametrize(
    "response,expected",
    [
        ("ON", True),
        # ("OFF", False),
    ]
)
def test_get_local_lock(system, device, response, expected):
    result = system.get_local_lock()
    assert result is expected


@pytest.mark.parametrize(
    "tone_command,flag,expected",
    [
        ("SYSTem:BEEPer:ALARm", True, "SYSTem:BEEPer:ALARm 1"),
        ("SYSTem:BEEPer:TOUCh", False, "SYSTem:BEEPer:TOUCh 0"),
    ]
)
def test_set_tones(system, device, tone_command, flag, expected):
    # We assume that set_warning_tone and set_keypad_tone use different commands.
    # Call the appropriate system method based on the tone_command.
    if device.connection.type == "wlan":
        pytest.skip(reason="Would change device state.")
    if tone_command.endswith("ALARm"):
        system.set_warning_tone(flag)
    else:
        system.set_keypad_tone(flag)
    assert device.command_log[-1] == expected
