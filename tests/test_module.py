"""Tests for the Additel SDK Module functionality."""

import pytest
from src.additel_sdk.module import DIModuleInfo
from src.additel_sdk.channel import DIFunctionChannelConfig
from conftest import compare_keys


def test_module_info(additel):
    """Test retrieval of module information."""
    info = additel.Module.info()
    assert isinstance(info, list), "Module info must be a list"
    assert all(
        isinstance(i, DIModuleInfo) for i in info
    ), "Module info must be a DIModuleInfo object"

    info_str = additel.Module.info_str()
    assert all(
        isinstance(x, DIModuleInfo) for x in info_str
    ), "Module info must be a DIModuleInfo object"
    compare_keys(info, info_str)


@pytest.mark.parametrize("module_index", [0, 1])
def test_query_channel_config(additel, module_index):
    """Test querying channel configuration."""
    config = additel.Module.getConfiguration(module_index=module_index)
    assert isinstance(config, list), "Channel config must be a list"
    for c in config:
        assert isinstance(
            c, DIFunctionChannelConfig
        ), "Channel config must be a DIFunctionChannelConfig object"


def test_query_channel_config_json(additel):
    """Test querying channel configuration in JSON format."""
    config = additel.Module.getConfiguration_json(module_index=0)
    assert isinstance(config, list), "Channel config must be a list"
    for c in config:
        assert isinstance(
            c, DIFunctionChannelConfig
        ), "Channel config must be a DIFunctionChannelConfig object"


def test_module_config(additel, module_config, module_config_json):
    """Test module configuration functionality."""
    compare_keys(module_config, module_config_json)


@pytest.mark.parametrize(
    "response,expected",
    [
        ('REF1,1,,102,1,0,1,10,4,AM1660,1624273,291f5ef50aff4ccabb4e2a421d6fd8e0,0,0;REF2,0,,3,1,0,1,10,4,Pt100(385),,,0,0;',
         ['REF1,1,,102,1,0,1,10,4,AM1660,1624273,291f5ef50aff4ccabb4e2a421d6fd8e0,0,0',
          'REF2,0,,3,1,0,1,10,4,Pt100(385),,,0,0']),  # RTD
    ],
)
def test_coerce_ChannelConfig(additel, response, expected):
    configs = DIFunctionChannelConfig.from_str(response)
    for conf, exp in zip(configs, expected):
        assert str(conf) == exp
