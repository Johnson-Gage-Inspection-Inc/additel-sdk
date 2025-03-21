"""Configuration file for pytest."""

import os
import sys
import pytest
from src.additel_sdk.base import Additel
from src.additel_sdk.channel import Channel
from src.additel_sdk.module import Module
from src.additel_sdk.scan import Scan
from unittest.mock import MagicMock

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Define device connection details
DEFAULT_IP = "192.168.1.223"


@pytest.fixture
def device_ip():
    """Get device IP from environment or use default."""
    return os.environ.get("ADDITEL_IP", DEFAULT_IP)


@pytest.fixture
def additel(device_ip):
    """Fixture to provide an Additel connection object."""
    with Additel("wlan", ip=device_ip) as device:
        yield device


@pytest.fixture
def module_config(device, module_index=0):
    """Fixture to provide module configuration."""
    mod = Module(device)
    return mod.getConfiguration(module_index=module_index)


@pytest.fixture
def module_config_json(device, module_index=0):
    """Fixture to provide module configuration in JSON format."""
    mod = Module(device)
    return mod.getConfiguration_json(module_index=module_index)


@pytest.fixture
def scan_config(device):
    """Fixture to provide scan configuration."""
    scan = Scan(device)
    return scan.get_configuration()


@pytest.fixture
def scan_config_json(device):
    """Fixture to provide scan configuration in JSON format."""
    scan = Scan(device)
    return scan.get_configuration_json()


@pytest.fixture
def channel_config(device, channel_name="REF1"):
    """Fixture to provide channel configuration."""
    chan = Channel(device)
    return chan.configure(channel_name)


# Helper functions
def compare_keys(a, b):
    """Helper function to compare keys between two objects."""
    for i, x in enumerate(a):
        for key in x.__dict__.keys():
            assert key in b[i].__dict__.keys(), f"Key {key} not found"
    for i, x in enumerate(b):
        for key in x.__dict__.keys():
            assert key in a[i].__dict__.keys(), f"Key {key} not found"


def pytest_addoption(parser):
    parser.addoption(
        "--real",
        action="store_true",
        default=False,
        help="Use real Additel device instead of mock",
    )


@pytest.fixture
def device(request, device_ip, mock_additel):
    if request.config.getoption("--real"):
        from src.additel_sdk.base import Additel  # import the real connection
        with Additel("wlan", ip=device_ip) as real_device:
            yield real_device
    else:
        yield mock_additel


@pytest.fixture
def mock_additel(monkeypatch):
    """Fixture that returns a mocked Additel object with a dummy connection.

    This fixture uses a dictionary of fake responses to emulate the Additel machine.
    """
    mock_device = MagicMock(spec=Additel)

    # Pre-defined responses for commands
    responses = {
        "*IDN?": "'685022040027',TAU-HOST 1.1.1.0",
        'CHANnel:CONFig? "REF1"': "REF1,1,,102,1,0,1,10,4,AM1660,1624273,291f5ef50aff4ccabb4e2a421d6fd8e0,0,0",
        'CHANnel:CONFig:JSON? "REF1,REF2"': (
            '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIFunctionChannelConfig, TAU.Module.Channels]], mscorlib",'
            '"$values":['
            '{"$type":"TAU.Module.Channels.DI.DIFunctionRTDChannelConfig, TAU.Module.Channels",'
            '"Wire":4,"CompensateInterval":0,"IsSquareRooting2Current":false,"IsCurrentCommutation":true,'
            '"SensorName":"AM1660","SensorSN":"1624273",'
            '"Id":"291f5ef50aff4ccabb4e2a421d6fd8e0","Name":"REF1","Enabled":true,"Label":"",'
            '"ElectricalFunctionType":102,"IsAutoRange":true,"Range":1,"Delay":0,"FilteringCount":10,'
            '"ChannelInfo1":"","ChannelInfo2":"","ChannelInfo3":"","ClassName":"DIFunctionRTDChannelConfig"},'
            '{"$type":"TAU.Module.Channels.DI.DIFunctionRTDChannelConfig, TAU.Module.Channels",'
            '"Wire":4,"CompensateInterval":0,"IsSquareRooting2Current":false,"IsCurrentCommutation":true,'
            '"SensorName":"Pt100(385)","SensorSN":"","Id":"","Name":"REF2","Enabled":false,"Label":"",'
            '"ElectricalFunctionType":3,"IsAutoRange":true,"Range":1,"Delay":0,"FilteringCount":10,'
            '"ChannelInfo1":"","ChannelInfo2":"","ChannelInfo3":"","ClassName":"DIFunctionRTDChannelConfig"}'
            ']}'
        ),
        'CHANnel:CONFig? "REF2"': "REF2,0,,3,1,0,1,10,4,Pt100(385),,,0,0",
        'JSON:MODule:INFormation?': '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIModuleInfo, TAU.Module.Channels]], mscorlib","$values":[{"$type":"TAU.Module.Channels.DI.DIModuleInfo, TAU.Module.Channels","Index":0,"Category":0,"SN":"","HwVersion":"","SwVersion":"","TotalChannelCount":2,"Label":null,"ClassName":"DIModuleInfo"},{"$type":"TAU.Module.Channels.DI.DIModuleInfo, TAU.Module.Channels","Index":1,"Category":1,"SN":"6851022030037","HwVersion":"TAU-M1 V01.00.00.00","SwVersion":"TAU-M1 V01.05","TotalChannelCount":20,"Label":null,"ClassName":"DIModuleInfo"}]}',
        'MODule:INFormation?': '0,,0,,,2,;1,6851022030037,1,TAU-M1 V01.00.00.00,TAU-M1 V01.05,20,',
        'MODule:CONFig? 0': "REF1,1,,102,1,0,1,10,4,AM1660,1624273,291f5ef50aff4ccabb4e2a421d6fd8e0,0,0;REF2,0,,3,1,0,1,10,4,Pt100(385),,,0,0;",
        'MODule:CONFig? 1': "CH1-01A,1,,100,0,0,0,10,0,K,,,0,0,;CH1-01B,1,,100,0,0,0,10,1,J,,,0,0,;CH1-02A,1,,100,0,0,0,10,1,T,,,0,0,;CH1-02B,1,,100,0,0,0,10,1,N,,,0,0,;CH1-03A,1,,100,0,0,0,10,1,N,,,0,0,;CH1-03B,1,,100,0,0,0,10,1,B,,,0,0,;CH1-04A,1,,100,0,0,0,10,1,N,,,0,0,;CH1-04B,1,,100,0,0,0,10,1,J,,,0,0,;CH1-05A,1,,100,0,0,0,10,1,J,,,0,0,;CH1-05B,1,,100,0,0,0,10,1,J,,,0,0,;CH1-06A,1,,100,0,0,0,10,1,K,,,0,0,;CH1-06B,1,,100,0,0,0,10,1,K,,,0,0,;CH1-07A,1,,100,0,0,0,10,1,K,,,0,0,;CH1-07B,1,,100,0,0,0,10,1,K,,,0,0,;CH1-08A,1,,100,0,0,0,10,1,K,,,0,0,;CH1-08B,1,,100,0,0,0,10,1,K,,,0,0,;CH1-09A,1,,100,0,0,0,10,1,K,,,0,0,;CH1-09B,1,,100,0,0,0,10,1,K,,,0,0,;CH1-10A,1,,100,0,0,0,10,1,K,,,0,0,;CH1-10B,1,,100,0,0,0,10,1,K,,,0,0,;",
        'JSON:MODule:CONFig? 0': '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIFunctionChannelConfig, TAU.Module.Channels]], mscorlib","$values":[{"$type":"TAU.Module.Channels.DI.DIFunctionRTDChannelConfig, TAU.Module.Channels","Wire":4,"CompensateInterval":0,"IsSquareRooting2Current":false,"IsCurrentCommutation":true,"SensorName":"AM1660","SensorSN":"1624273","Id":"291f5ef50aff4ccabb4e2a421d6fd8e0","Name":"REF1","Enabled":true,"Label":"","ElectricalFunctionType":102,"IsAutoRange":true,"Range":1,"Delay":0,"FilteringCount":10,"ChannelInfo1":"","ChannelInfo2":"","ChannelInfo3":"","ClassName":"DIFunctionRTDChannelConfig"},{"$type":"TAU.Module.Channels.DI.DIFunctionRTDChannelConfig, TAU.Module.Channels","Wire":4,"CompensateInterval":0,"IsSquareRooting2Current":false,"IsCurrentCommutation":true,"SensorName":"Pt100(385)","SensorSN":"","Id":"","Name":"REF2","Enabled":false,"Label":"","ElectricalFunctionType":3,"IsAutoRange":true,"Range":1,"Delay":0,"FilteringCount":10,"ChannelInfo1":"","ChannelInfo2":"","ChannelInfo3":"","ClassName":"DIFunctionRTDChannelConfig"}]}',
        'SCAN:STARt?': "1000,REF1",
        'JSON:SCAN:STARt?': '{"$type":"TAU.Module.Channels.DI.DIScanInfo, TAU.Module.Channels","ChannelName":"REF1","NPLC":1000,"ClassName":"DIScanInfo"}',
        'JSON:SCAN:DATA? 1': '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIReading, TAU.Module.Channels]], mscorlib","$values":[{"$type":"TAU.Module.Channels.DI.DITemperatureReading, TAU.Module.Channels","TempValues":{"$type":"System.Collections.Generic.List`1[[System.Double, mscorlib]], mscorlib","$values":[22.550004760925106]},"TempUnit":1001,"TempDecimals":4,"ChannelName":"REF1","Values":{"$type":"System.Collections.Generic.List`1[[System.Double, mscorlib]], mscorlib","$values":[109.05974453720414]},"ValuesFiltered":{"$type":"System.Collections.Generic.List`1[[System.Double, mscorlib]], mscorlib","$values":[109.06087137980892]},"DateTimeTicks":{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.TimeTick, TAU.Module.Channels]], mscorlib","$values":[{"$type":"TAU.Module.Channels.DI.TimeTick, TAU.Module.Channels","TickTime":"2025-03-21 18:02:48 320"}]},"Unit":1281,"ValueDecimals":6,"ClassName":"DITemperatureReading"}]}',
        'JSON:SCAN:DATA? 2': '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIReading, TAU.Module.Channels]], mscorlib","$values":[{"$type":"TAU.Module.Channels.DI.DITemperatureReading, TAU.Module.Channels","TempValues":{"$type":"System.Collections.Generic.List`1[[System.Double, mscorlib]], mscorlib","$values":[22.547161948563378,22.547770774579941]},"TempUnit":1001,"TempDecimals":4,"ChannelName":"REF1","Values":{"$type":"System.Collections.Generic.List`1[[System.Double, mscorlib]], mscorlib","$values":[109.05874917092972,109.05890529343073]},"ValuesFiltered":{"$type":"System.Collections.Generic.List`1[[System.Double, mscorlib]], mscorlib","$values":[109.05974453720414,109.05998586563665]},"DateTimeTicks":{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.TimeTick, TAU.Module.Channels]], mscorlib","$values":[{"$type":"TAU.Module.Channels.DI.TimeTick, TAU.Module.Channels","TickTime":"2025-03-21 18:02:57 680"},{"$type":"TAU.Module.Channels.DI.TimeTick, TAU.Module.Channels","TickTime":"2025-03-21 18:02:56 640"}]},"Unit":1281,"ValueDecimals":6,"ClassName":"DITemperatureReading"}]}',
        'SCAN:DATA:Last? 2': '"REF1,1281,1,638781769683200000,109.059745,109.060871,1001,1,22.5500;"',
        'JSON:SCAN:SCONnection:DATA? 1': '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIReading, TAU.Module.Channels]], mscorlib","$values":[]}',
    }

    def fake_cmd(command):
        # Return the fake response if available
        return responses.get(command, "OK")

    mock_device.cmd.side_effect = fake_cmd
    mock_device.connection = MagicMock()
    mock_device.connection.connection = True

    return mock_device
