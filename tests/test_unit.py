from src.additel_sdk.unit import Unit


def test_get_unit_temp_success(device):
    # When parent.cmd returns a valid response, get_unit_temp should return the split 
    # list.
    unit = Unit(device)
    unit_temp = unit.get_unit_temp()
    assert unit_temp is not None, "Expected ValueError but got None"
