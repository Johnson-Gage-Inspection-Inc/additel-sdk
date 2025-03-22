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

def test_getstate_true(bluetooth_fixture):
    state = bluetooth_fixture.getstate()
    assert state in ["ON", "OFF"], "Expected 'ON' or 'OFF' but got something else."

def test_getstate_no_response(bluetooth_fixture, monkeypatch):
    # Simulate no response from the parent's cmd method.
    monkeypatch.setattr(bluetooth_fixture.parent, "cmd", lambda command: "")
    with pytest.raises(ValueError, match="No Bluetooth state information returned."):
        bluetooth_fixture.getstate()

def test_getName(bluetooth_fixture):
    name = bluetooth_fixture.getName()
    assert name == "Compact"

def test_getName_no_response(bluetooth_fixture, monkeypatch):
    # Simulate no response for the name query.
    monkeypatch.setattr(bluetooth_fixture.parent, "cmd", lambda command: "")
    with pytest.raises(ValueError, match="No Bluetooth name information returned."):
        bluetooth_fixture.getName()

@pytest.mark.skip(reason="Not yet implemented")
def test_setName(bluetooth_fixture):
    new_name = "NewName"
    bluetooth_fixture.setName(new_name)
    assert bluetooth_fixture.parent.commands[-1] == f"SYSTem:COMMunicate:BLUEtooth:NAMe {new_name}"