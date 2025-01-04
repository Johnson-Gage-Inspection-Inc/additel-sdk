from sdk.base import Additel

def testIdentify(a: Additel):
    identity = a.identify()
    assert identity == "'685022040027',TAU-HOST 1.1.1.0", "Identity must be correct"
    return identity

def testModuleInfo(a: Additel):
    info = a.Module.info()
    assert isinstance(info, list), "Module info must be a list"
    assert all(isinstance(i, a.DI.DIModuleInfo) for i in info), "Module info must be a DIModuleInfo object"

    info_str = a.Module.info_str()
    assert all(isinstance(x, a.DI.DIModuleInfo) for x in info_str), "Module info must be a DIModuleInfo object"
    compare_keys(info, info_str)
    return info

def testQueryChannelConfig(a: Additel, module_index=0):
    config = a.Module.getConfiguration(module_index=module_index)
    assert isinstance(config, list), "Channel config must be a list"
    for c in config:
        assert isinstance(c, a.DI.DIFunctionChannelConfig), "Channel config must be a DIFunctionChannelConfig object"
    return config

def testQueryChannelConfig_json(a: Additel, module_index=0):
    config = a.Module.getConfiguration_json(module_index=module_index)
    assert isinstance(config, list), "Channel config must be a list"
    for c in config:
        assert isinstance(c, a.DI.DIFunctionChannelConfig), "Channel config must be a DIFunctionChannelConfig object"
    return config

def testModuleConfig(additel):  # Tested!
    config1 = testQueryChannelConfig(additel)
    configfromjson1 = testQueryChannelConfig_json(additel)
    compare_keys(config1, configfromjson1)
    config2 = testQueryChannelConfig(additel, 1)
    return config2
    # configfromjson2 = testQueryChannelConfig_json(additel, 1)  # This doesn't work because the response gets cut off
    # compare_keys(config2, configfromjson2)

def compare_keys(a, b):
    for i, x in enumerate(a):
        for key in x.keys():
            assert key in b[i].keys(), f"Key {key} not found"
    for i, x in enumerate(b):
        for key in x.keys():
            assert key in a[i].keys(), f"Key {key} not found"

def testScanGetConfigJson(a: Additel):
    scan_config = a.Scan.get_configuration_json()
    assert isinstance(scan_config, a.DI.DIScanInfo), "Scan config must be a DIScanInfo object"
    return scan_config

def testScanGetConfig(a: Additel):
    scan_config = a.Scan.get_configuration()
    assert isinstance(scan_config, a.DI.DIScanInfo), "Scan config must be a DIScanInfo object"
    return scan_config

def testScan(additel):
    scanTestJson = testScanGetConfigJson(additel)
    scanTest = testScanGetConfig(additel)
    assert str(scanTestJson) == str(scanTest), "Scan config from json and scan config from string are not equal"
    assert scanTestJson == scanTest, "Scan config from json and scan config from string are not equal"
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

def testGetChannelConfig(a: Additel):
    config = a.Channel.get_configuration('REF1')
    assert isinstance(config, a.DI.DIFunctionChannelConfig), "Channel config must be a DIFunctionChannelConfig object"
    return config

def testGetChannelConfig_json(a: Additel):
    config = a.Channel.get_configuration_json(['REF1', 'REF2'])
    assert all(isinstance(x, a.DI.DIFunctionChannelConfig) for x in config), "Channel config must be a DIFunctionChannelConfig object"
    return config

if __name__ == '__main__':
    # Create an instance of the Additel class
    with Additel('192.168.1.223') as additel:
        identity = testIdentify(additel)
        moduleInfo = testModuleInfo(additel)
        testModuleConfig(additel)
        testScan(additel)
        testScanLast()
        channelConfig = testGetChannelConfig(additel)
        channelConfigJson = testGetChannelConfig_json(additel)
        # additel.Channel.configure(channelConfigJson[0])

        print("All tests passed!")
