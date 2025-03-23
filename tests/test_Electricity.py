import pytest
from src.additel_sdk.calibration import Electricity

@pytest.fixture
def electricity_fixture(device) -> Electricity:
    return Electricity(device)


def test_valid_response_status(electricity_fixture):
    expected = {
        'exception_code': '0',
        'mode': '0',
        'function': '0',
        'range': '0',
        'status': '0',
        'data': None
        }
    result = electricity_fixture.get_scan_data()
    assert result == expected, f"Expected {expected} but got {result}"
