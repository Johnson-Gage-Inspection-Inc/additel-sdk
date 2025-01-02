from sdk.base import Additel

def testIdentify(a: Additel):
    identity = a.identify()
    assert identity == "'685022040027',TAU-HOST 1.1.1.0", "Identity is not correct"
    return identity

def testModuleInfo(a: Additel):
    info = a.Module.info()
    assert isinstance(info, list), "Module info is not a list"
    for i in info:
        assert isinstance(i, a.DI.DIModuleInfo), "Module info is not a DIModuleInfo object"
    return info

def testQueryChannelConfig(a: Additel, module_index=0):
    config = a.Module.getConfiguration(module_index=module_index)
    assert isinstance(config, list), "Channel config is not a list"
    for c in config:
        assert isinstance(c, a.DI.DIFunctionChannelConfig), "Channel config is not a DIFunctionChannelConfig object"
    return config

def testQueryChannelConfig_json(a: Additel, module_index=0):
    config = a.Module.getConfiguration(module_index=module_index)
    assert isinstance(config, list), "Channel config is not a list"
    for c in config:
        assert isinstance(c, a.DI.DIFunctionChannelConfig), "Channel config is not a DIFunctionChannelConfig object"
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

def testScanGetConfig(a: Additel):
    scan_config = a.Scan.get_configuration_json()
    assert isinstance(scan_config, a.DI.DIScanInfo), "Scan config is not a DIScanInfo object"
    return scan_config

if __name__ == '__main__':
    # Create an instance of the Additel class
    with Additel('192.168.1.222') as additel:
        identity = testIdentify(additel)
        moduleInfo = testModuleInfo(additel)
        testModuleConfig(testQueryChannelConfig, additel)
        scanTest = testScanGetConfig(additel)


        pass
