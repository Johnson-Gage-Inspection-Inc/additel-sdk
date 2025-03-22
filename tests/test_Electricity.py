from src.additel_sdk.calibration import Electricity


def test_valid_response_status_1(device):
    # given a valid response with status "1"
    # response format: exception_code,mode,function,range,status,data
    elec = Electricity(device)
    
    result = elec.get_scan_data()
    assert result == {'exception_code': '0', 'mode': '0', 'function': '0', 'range': '0', 'status': '0', 'data': None}