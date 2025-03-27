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
    if result['status'] == 1:
        zipped = zip(result.items(), expected.items())
        for key in zipped:
            assert key[0] == key[1]
        return
    assert not diff, diff
