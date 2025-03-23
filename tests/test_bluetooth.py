import pytest
from src.additel_sdk.system.communicate.bluetooth import Bluetooth

@pytest.fixture
def bluetooth_fixture(device) -> Bluetooth:
    return Bluetooth(device)

@pytest.mark.skip(reason="Not yet implemented")
def test_set_state_enable(bluetooth_fixture):
    bluetooth_fixture.set_state(True)
    assert bluetooth_fixture.parent.commands[-1] == "SYSTem:COMMunicate:SOCKet:BLUetooth:STATe 1"

@pytest.mark.skip(reason="Not yet implemented")
def test_set_state_disable(bluetooth_fixture):
    bluetooth_fixture.set_state(False)
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
    original_name = bluetooth_fixture.get_name()
    new_name = "NewName"
    bluetooth_fixture.set_name(new_name)
    is_name_set_correctly = bluetooth_fixture.parent.commands[-1] == f"SYSTem:COMMunicate:BLUEtooth:NAMe {new_name}"

    # Reset to original name before asserting
    bluetooth_fixture.set_name(original_name)  
    assert is_name_set_correctly, f"Expected '{new_name}' but got {bluetooth_fixture.parent.commands[-1]}"
    assert original_name == bluetooth_fixture.get_name()