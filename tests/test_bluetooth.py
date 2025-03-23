import pytest
from src.additel_sdk.system.communicate.bluetooth import Bluetooth

@pytest.fixture
def bluetooth_fixture(device):
    return Bluetooth(device)

@pytest.mark.skip(reason="Not yet implemented")
def test_setstate_enable(bluetooth_fixture):
    bluetooth_fixture.setstate(True)
    assert bluetooth_fixture.parent.commands[-1] == "SYSTem:COMMunicate:SOCKet:BLUetooth:STATe 1"

@pytest.mark.skip(reason="Not yet implemented")
def test_setstate_disable(bluetooth_fixture):
    bluetooth_fixture.setstate(False)
    assert bluetooth_fixture.parent.commands[-1] == "SYSTem:COMMunicate:SOCKet:BLUetooth:STATe 0"

def test_get_state_true(bluetooth_fixture):
    state = bluetooth_fixture.get_state()
    assert state in ["ON", "OFF"], "Expected 'ON' or 'OFF' but got something else."

def test_get_state_no_response(bluetooth_fixture, monkeypatch):
    # Simulate no response from the parent's cmd method.
    monkeypatch.setattr(bluetooth_fixture.parent, "cmd", lambda command: "")
    with pytest.raises(ValueError, match="No Bluetooth state information returned."):
        bluetooth_fixture.get_state()

def test_get_name(bluetooth_fixture):
    name = bluetooth_fixture.get_name()
    assert name == "Compact"

def test_get_name_no_response(bluetooth_fixture, monkeypatch):
    # Simulate no response for the name query.
    monkeypatch.setattr(bluetooth_fixture.parent, "cmd", lambda command: "")
    with pytest.raises(ValueError, match="No Bluetooth name information returned."):
        bluetooth_fixture.get_name()

@pytest.mark.skip(reason="Not yet implemented")
def test_set_name(bluetooth_fixture):
    new_name = "NewName"
    bluetooth_fixture.set_name(new_name)
    assert bluetooth_fixture.parent.commands[-1] == f"SYSTem:COMMunicate:BLUEtooth:NAMe {new_name}"