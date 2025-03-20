"""Tests for the Additel SDK Channel functionality."""

import pytest
from sdk.channel import DIFunctionChannelConfig


def test_get_channel_config(additel):
    """Test retrieval of channel configuration."""
    config = additel.Channel.get_configuration("REF1")
    assert isinstance(
        config, DIFunctionChannelConfig
    ), "Channel config must be a DIFunctionChannelConfig object"
    assert config["Name"] == "REF1", "Channel name should be REF1"


def test_get_channel_config_json(additel):
    """Test retrieval of channel configuration in JSON format."""
    config = additel.Channel.get_configuration_json(["REF1", "REF2"])
    assert isinstance(config, list), "Config should be a list"
    assert len(config) == 2, "Should return 2 configurations"
    assert all(
        isinstance(x, DIFunctionChannelConfig) for x in config
    ), "Each config must be a DIFunctionChannelConfig object"
    assert config[0]["Name"] == "REF1", "First config should be for REF1"
    assert config[1]["Name"] == "REF2", "Second config should be for REF2"


@pytest.mark.skip(reason="Not yet implemented")
def test_channel_configure(additel, channel_config):
    """Test channel configuration (currently disabled)."""
    additel.Channel.configure(channel_config)


@pytest.mark.parametrize(
    "channel_name,expected_type",
    [
        ("REF1", 102),  # Voltage
        ("REF2", 3),  # RTD type
    ],
)
def test_channel_types(additel, channel_name, expected_type):
    config = additel.Channel.get_configuration(channel_name)
    assert config["ElectricalFunctionType"] == expected_type
