from sdk.base import Additel

def testIdentify(a: Additel):
    identity = a.identify()
    assert identity == "'685022040027',TAU-HOST 1.1.1.0", "Identity is not correct"
    return identity

def testModuleInfo(a: Additel):
    info = a.Module.info()
    assert isinstance(info, list), "Module info is not a list"
    for i in info:
        assert isinstance(i, a.type.DIModuleInfo), "Module info is not a DIModuleInfo object"
    return info

def testQueryChannelConfig(a: Additel):
    config = a.Module.getConfiguration(module_index=1)
    assert isinstance(config, list), "Channel config is not a list"
    for c in config:
        assert isinstance(c, a.type.DIFunctionChannelConfig), "Channel config is not a DIFunctionChannelConfig object"
    return config

def testQueryChannelConfig_json(a: Additel):
    config = a.Module.getConfiguration_json(module_index=0)
    assert isinstance(config, list), "Channel config is not a list"
    for c in config:
        assert isinstance(c, a.type.DIFunctionChannelConfig), "Channel config is not a DIFunctionChannelConfig object"
    return config

if __name__ == '__main__':
    # Create an instance of the Additel class
    with Additel('192.168.1.222') as additel:
        identity = testIdentify(additel)
        print("Identity check passed.")
        moduleInfo = testModuleInfo(additel)  # Passed
        print("Module info check passed.")
        config = testQueryChannelConfig(additel)  # Passed
        print("Query channel config check passed.")
        config_json = testQueryChannelConfig_json(additel)
        print("Query channel config json check passed.")
        pass
