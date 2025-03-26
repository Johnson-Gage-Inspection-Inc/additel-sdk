"""Tests for the Additel SDK Channel functionality."""

import pytest
from src.additel_sdk.channel import Channel, DIFunctionChannelConfig
from src.additel_sdk.coerce import coerce


def test_get_channel_config(device):
    """Test retrieval of channel configuration."""
    chan = Channel(device)
    config = chan.get_configuration("REF1")
    assert isinstance(
        config, DIFunctionChannelConfig
    ), "Channel config must be a DIFunctionChannelConfig object"
    assert config.Name == "REF1", "Channel name should be REF1"


def test_get_channel_config_json(device):
    """Test retrieval of channel configuration in JSON format."""
    chan = Channel(device)
    configs = chan.get_configuration_json(Channel.valid_names)
    assert isinstance(configs, list), "Config should be a list"
    assert len(configs) == len(Channel.valid_names), "Should return 2 configurations"
    for name, config in zip(Channel.valid_names, configs):
        warning = "Config should be a DIFunctionChannelConfig object"
        assert isinstance(config, DIFunctionChannelConfig), warning
        assert name == config.Name, "Config name should match channel name"


@pytest.mark.skip(reason="Not yet implemented")
def test_channel_configure(device, channel_config):
    """Test channel configuration (currently disabled)."""
    chan = Channel(device)
    chan.configure(channel_config)


@pytest.mark.parametrize(
    "channel_name,expected_type",
    [
        ("REF1", 102),  # SPRT
        ("REF2", 3),  # RTD type
    ],
)
def test_channel_types(device, channel_name, expected_type):
    chan = Channel(device)
    config = chan.get_configuration(channel_name)
    assert config.ElectricalFunctionType == expected_type


@pytest.mark.parametrize(
    "file,expected",
    [
        (
            "RTDChannelConfigList.json",
            [
                "REF1,1,,102,1,0,1,10,4,AM1660,1624273,291f5ef50aff4ccabb4e2a421d6fd8e0,0,0",
                "REF2,0,,3,1,0,1,10,4,Pt100(385),,,0,0",
            ],
        ),  # RTD
    ],
)
def test_coerce_ChannelConfig(file, expected):
    test_data_dir = "tests/testdata/"
    with open(test_data_dir + file, "r") as f:
        config = f.read()
    coerced_config = coerce(config)
    for conf, exp in zip(coerced_config, expected):
        assert str(conf) == exp
