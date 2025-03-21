"""Tests for the Additel SDK Module functionality."""

import pytest
from src.additel_sdk.module import DIModuleInfo, Module
from src.additel_sdk.channel import DIFunctionChannelConfig, DIFunctionTCChannelConfig
from conftest import compare_keys


def test_module_info(device):
    """Test retrieval of module information."""
    mod = Module(device)
    info = mod.info()
    assert isinstance(info, list), "Module info must be a list"
    assert all(
        isinstance(i, DIModuleInfo) for i in info
    ), "Module info must be a DIModuleInfo object"

    info_str = mod.info_str()
    assert all(
        isinstance(x, DIModuleInfo) for x in info_str
    ), "Module info must be a DIModuleInfo object"
    compare_keys(info, info_str)


@pytest.mark.parametrize("module_index", [0, 1])
def test_query_channel_config(device, module_index):
    """Test querying channel configuration."""
    mod = Module(device)
    config = mod.getConfiguration(module_index=module_index)
    assert isinstance(config, list), "Channel config must be a list"
    for c in config:
        assert isinstance(
            c, DIFunctionChannelConfig
        ), "Channel config must be a DIFunctionChannelConfig object"


def test_query_channel_config_json(device):
    """Test querying channel configuration in JSON format."""
    mod = Module(device)
    config = mod.getConfiguration_json(module_index=0)
    assert isinstance(config, list), "Channel config must be a list"
    for c in config:
        assert isinstance(
            c, DIFunctionChannelConfig
        ), "Channel config must be a DIFunctionChannelConfig object"


def test_module_config(module_config, module_config_json):
    """Test module configuration functionality."""
    compare_keys(module_config, module_config_json)


@pytest.mark.parametrize(
    "response,expected",
    [
        (
            "REF1,1,,102,1,0,1,10,4,AM1660,1624273,291f5ef50aff4ccabb4e2a421d6fd8e0,0,0;REF2,0,,3,1,0,1,10,4,Pt100(385),,,0,0;",
            [
                "REF1,1,,102,1,0,1,10,4,AM1660,1624273,291f5ef50aff4ccabb4e2a421d6fd8e0,0,0",
                "REF2,0,,3,1,0,1,10,4,Pt100(385),,,0,0",
            ],
        ),  # RTD
    ],
)
def test_coerce_ChannelConfig(response, expected):
    configs = DIFunctionChannelConfig.from_str(response)
    for conf, exp in zip(configs, expected):
        assert str(conf) == exp


@pytest.fixture
def expected_tc_channel_config():
    return [
        {
            "Name": name,
            "SensorName": sensor,
            "IsOpenDetect": iod,
            "Enabled": 1,
            "Label": None,
            "ElectricalFunctionType": 100,
            "Range": 0,
            "Delay": 0,
            "IsAutoRange": 0,
            "FilteringCount": 10,
            "IsCurrentCommutation": None,
            "ChannelInfo1": None,
            "ChannelInfo2": None,
            "ChannelInfo3": None,
            "CjcType": None,
            "CJCFixedValue": None,
            "CjcChannelName": '0',
        } for name, sensor, iod in [
            ('CH1-01A', 'K', 0), ('CH1-01B', 'J', 1), ('CH1-02A', 'T', 1), ('CH1-02B', 'N', 1),
            ('CH1-03A', 'N', 1), ('CH1-03B', 'B', 1), ('CH1-04A', 'N', 1), ('CH1-04B', 'J', 1),
            ('CH1-05A', 'J', 1), ('CH1-05B', 'J', 1), ('CH1-06A', 'K', 1), ('CH1-06B', 'K', 1),
            ('CH1-07A', 'K', 1), ('CH1-07B', 'K', 1), ('CH1-08A', 'K', 1), ('CH1-08B', 'K', 1),
            ('CH1-09A', 'K', 1), ('CH1-09B', 'K', 1), ('CH1-10A', 'K', 1), ('CH1-10B', 'K', 1),
        ]
    ]


@pytest.mark.parametrize(
    "response",
    [
        "CH1-01A,1,,100,0,0,0,10,0,K,,,0,0,;CH1-01B,1,,100,0,0,0,10,1,J,,,0,0,;CH1-02A,1,,100,0,0,0,10,1,T,,,0,0,;CH1-02B,1,,100,0,0,0,10,1,N,,,0,0,;CH1-03A,1,,100,0,0,0,10,1,N,,,0,0,;CH1-03B,1,,100,0,0,0,10,1,B,,,0,0,;CH1-04A,1,,100,0,0,0,10,1,N,,,0,0,;CH1-04B,1,,100,0,0,0,10,1,J,,,0,0,;CH1-05A,1,,100,0,0,0,10,1,J,,,0,0,;CH1-05B,1,,100,0,0,0,10,1,J,,,0,0,;CH1-06A,1,,100,0,0,0,10,1,K,,,0,0,;CH1-06B,1,,100,0,0,0,10,1,K,,,0,0,;CH1-07A,1,,100,0,0,0,10,1,K,,,0,0,;CH1-07B,1,,100,0,0,0,10,1,K,,,0,0,;CH1-08A,1,,100,0,0,0,10,1,K,,,0,0,;CH1-08B,1,,100,0,0,0,10,1,K,,,0,0,;CH1-09A,1,,100,0,0,0,10,1,K,,,0,0,;CH1-09B,1,,100,0,0,0,10,1,K,,,0,0,;CH1-10A,1,,100,0,0,0,10,1,K,,,0,0,;CH1-10B,1,,100,0,0,0,10,1,K,,,0,0,;",
    ],
)
def test_coerce_ChannelConfig_TC(response, expected_tc_channel_config):
    actual = DIFunctionChannelConfig.from_str(response)
    for a, e in zip(actual, expected_tc_channel_config):
        assert a == DIFunctionTCChannelConfig(**e)
