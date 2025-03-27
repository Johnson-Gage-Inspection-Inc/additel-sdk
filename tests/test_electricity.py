import pytest
from src.additel_sdk.calibration import Electricity
from deepdiff import DeepDiff


@pytest.fixture
def electricity_fixture(device) -> Electricity:
    return Electricity(device)


def test_valid_response_status(electricity_fixture: Electricity):
    expected = {
        "exception_code": "0",
        "mode": "0",
        "function": "0",
        "range": "0",
        "status": "0",
        "data": None,
    }
    result = electricity_fixture.get_scan_data()
    diff = DeepDiff(result, expected, ignore_order=True)
    if result['status'] == '1':
        assert result['exception_code'] == '0', "Exception code should be 0"
        assert result['mode'] == '0', "Mode should be 0"
        assert result['function'] == '0', "Function should be 0"
        assert result['range'] == '0', "Range should be 0"
        assert result['data'] is not None, "Data should not be None"
    else:
        assert not diff, diff
