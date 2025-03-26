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
        "status": "1",
        "data": 114.442191207159,
    }
    result = electricity_fixture.get_scan_data()
    diff = DeepDiff(result, expected)
    assert not diff, f"Unexpected response: {diff}"
