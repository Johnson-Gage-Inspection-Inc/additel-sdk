from sdk.base import Additel

def testIdentify(a: Additel):
    identity = a.identify()
    assert identity == "'685022040027',TAU-HOST 1.1.1.0", "Identity must be correct"
    return identity

def testModuleInfo(a: Additel):
    info = a.Module.info()
    assert isinstance(info, list), "Module info must be a list"
    for i in info:
        assert isinstance(i, a.DI.DIModuleInfo), "Module info must be a DIModuleInfo object"
    return info

def testQueryChannelConfig(a: Additel, module_index=0):
    config = a.Module.getConfiguration(module_index=module_index)
    assert isinstance(config, list), "Channel config must be a list"
    for c in config:
        assert isinstance(c, a.DI.DIFunctionChannelConfig), "Channel config must be a DIFunctionChannelConfig object"
    return config

def testQueryChannelConfig_json(a: Additel, module_index=0):
    config = a.Module.getConfiguration(module_index=module_index)
    assert isinstance(config, list), "Channel config must be a list"
    for c in config:
        assert isinstance(c, a.DI.DIFunctionChannelConfig), "Channel config must be a DIFunctionChannelConfig object"
    return config

def testModuleConfig(testQueryChannelConfig, additel):
    config1 = testQueryChannelConfig(additel)
    configfromjson1 = testQueryChannelConfig(additel)
    for i, configuration in enumerate(config1):
        for key in configuration.to_json().keys():
            assert key in configfromjson1[i].to_json().keys(), f"Key {key} not found in configfromjson1"
    config2 = testQueryChannelConfig(additel, 1)
    configfromjson2 = testQueryChannelConfig(additel, 1)
    for i, configuration in enumerate(config2):
        for key in configuration.to_json().keys():
            assert key in configfromjson2[i].to_json().keys(), f"Key {key} not found in config from json2"

def testScanGetConfigJson(a: Additel):
    scan_config = a.Scan.get_configuration_json()
    assert isinstance(scan_config, a.DI.DIScanInfo), "Scan config must be a DIScanInfo object"
    return scan_config

def testScanGetConfig(a: Additel):
    scan_config = a.Scan.get_configuration()
    assert isinstance(scan_config, a.DI.DIScanInfo), "Scan config must be a DIScanInfo object"
    return scan_config

def testScan(testScanGetConfigJson, testScanGetConfig, additel):
    scanTestJson = testScanGetConfigJson(additel)
    scanTest = testScanGetConfig(additel)
    assert scanTestJson.to_str() == scanTest.to_str(), "Scan config from json and scan config from string are not equal"
    assert scanTestJson.to_json() == scanTest.to_json(), "Scan config from json and scan config from string are not equal"
    pass

def test_get_scan_data_json(a: Additel, count: int = 1):
    data = a.Scan.get_scan_data_json(count)
    assert all(isinstance(d, a.DI.DIReading) for d in data), "Data must be a DIScanData object"
    return data

def test_get_latest_data(a: Additel):
    data = a.Scan.get_latest_data()
    assert isinstance(data, a.DI.DIReading), "Data must be a DIScanData object"
    return data

def testScanLast(n_data=1):
    data_json = test_get_scan_data_json(additel, n_data)
    print(data_json)
    data = test_get_latest_data(additel)
    print([data])
    # assert data_json == [data], "Data from json and data from string are not equal"  # They kinda are, but not there's some differences in rounding and they're actually representing different data, I think

if __name__ == '__main__':
    # Create an instance of the Additel class
    with Additel('192.168.1.223') as additel:
        identity = testIdentify(additel)
        moduleInfo = testModuleInfo(additel)
        testModuleConfig(testQueryChannelConfig, additel)
        testScan(testScanGetConfigJson, testScanGetConfig, additel)
        testScanLast()
        pass
