"""Tests for the base Additel SDK functionality."""

import pytest
from datetime import date


def test_identify(device):
    """Test device identification functionality."""
    identity = device.identify()
    assert identity == "'685022040027',TAU-HOST 1.1.1.0", "Identity must be correct"


def test_connection(device):
    """Test that connection is properly established."""
    assert device.connection is not None, "Connection was not established"


@pytest.mark.parametrize(
    "command,expected",
    [
        ("*IDN?", "'685022040027',TAU-HOST 1.1.1.0"),
        ("UNIT:TEMPerature?", '°F,1002'),
        ("DISPlay:THEMe:ALLNames?", 'Dark,Light'),
        ("DISPlay:THEMe?", "Dark"),
        ("DISPlay:HOME?", "1"),
        ("DISPlay:LANGuage?", "en-US"),
        ("SYSTem:COMMunicate:BLUEtooth:NAMe?", "Compact"),
        ("SYSTem:COMMunicate:BLUEtooth?", "0"),
        ("SYSTem:PASSword:ENABle:SENSor?", "0"),
        ("SYSTem:COMMunicate:SOCKet:ETHernet:PHYSicaladdress?", "64:33:DB:73:A9:5F"),
        ("SYSTem:COMMunicate:SOCKet:ETHernet:GATeway?", "0.0.0.0"),
        ("SYSTem:COMMunicate:SOCKet:ETHernet:MASK?", "255.255.255.0"),
        ("SYSTem:COMMunicate:SOCKet:ETHernet:ADDRess?", "192.168.0.182"),
        ("SYSTem:COMMunicate:SOCKet:ETHernet:DHCP?", "0"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:CONNect?", "Connected"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:SSID?", '"JGI Production WiFi:WEP_OFF"'),
        ("SYSTem:COMMunicate:SOCKet:WLAN:DHCP:STATe?", "1"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:DHCP?", "1"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:MAC?", "C0:EE:40:15:67:7F"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:GATeway?", "192.168.1.1"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:MASK?", "255.255.255.0"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:ADDRess?", "192.168.1.223"),
        ("SYSTem:COMMunicate:SOCKet:WLAN?", "1"),
        ("SYSTem:COMMunicate:SOCKet:WLAN:STATe?", "1"),
        ("SYSTem:KLOCk?", "0"),
        ("SYSTem:DATE?", date.today().strftime("%Y,%m,%d")),
        ("CALibration:ElECtricity:SCAN?", "0,0,0,0,0,"),
        ("JSON:MEASure:SCAN:SCONnection:DATA? 1", '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIReading, TAU.Module.Channels]], mscorlib","$values":[]}'),
        ("JSON:MEASure:SCAN:SCONnection:DATA? 2", '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIReading, TAU.Module.Channels]], mscorlib","$values":[]}'),
        ("JSON:MEASure:SCAN:SCONnection:DATA? 3", '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIReading, TAU.Module.Channels]], mscorlib","$values":[]}'),
        ("JSON:SCAN:SCONnection:DATA? 1", '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIReading, TAU.Module.Channels]], mscorlib","$values":[]}'),
        ("JSON:SCAN:SCONnection:DATA? 2", '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIReading, TAU.Module.Channels]], mscorlib","$values":[]}'),
        ("JSON:SCAN:SCONnection:DATA? 3", '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIReading, TAU.Module.Channels]], mscorlib","$values":[]}'),
        ('MEASure:CHANnel:CONFig:JSON? "REF1"', '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIFunctionChannelConfig, TAU.Module.Channels]], mscorlib","$values":[{"$type":"TAU.Module.Channels.DI.DIFunctionRTDChannelConfig, TAU.Module.Channels","Wire":4,"CompensateInterval":0,"IsSquareRooting2Current":false,"IsCurrentCommutation":true,"SensorName":"AM1660","SensorSN":"1624273","Id":"291f5ef50aff4ccabb4e2a421d6fd8e0","Name":"REF1","Enabled":true,"Label":"","ElectricalFunctionType":102,"IsAutoRange":true,"Range":1,"Delay":0,"FilteringCount":10,"ChannelInfo1":"","ChannelInfo2":"","ChannelInfo3":"","ClassName":"DIFunctionRTDChannelConfig"}]}'),
        ("JSON:SCAN:STARt?", '{"$type":"TAU.Module.Channels.DI.DIScanInfo, TAU.Module.Channels","ChannelName":"REF1","NPLC":1000,"ClassName":"DIScanInfo"}'),
        ("JSON:MEASure:SCAN:STARt?", '{"$type":"TAU.Module.Channels.DI.DIScanInfo, TAU.Module.Channels","ChannelName":"REF1","NPLC":1000,"ClassName":"DIScanInfo"}'),
        ("MEASure:SCAN:STARt?", "1000,REF1"),
        ("SCAN:STARt?", "1000,REF1"),
        ("JSON:MEASure:MODule:INFormation?", '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIModuleInfo, TAU.Module.Channels]], mscorlib","$values":[{"$type":"TAU.Module.Channels.DI.DIModuleInfo, TAU.Module.Channels","Index":0,"Category":0,"SN":"","HwVersion":"","SwVersion":"","TotalChannelCount":2,"Label":null,"ClassName":"DIModuleInfo"},{"$type":"TAU.Module.Channels.DI.DIModuleInfo, TAU.Module.Channels","Index":1,"Category":1,"SN":"6851022030037","HwVersion":"TAU-M1 V01.00.00.00","SwVersion":"TAU-M1 V01.05","TotalChannelCount":20,"Label":null,"ClassName":"DIModuleInfo"}]}'),
        ("JSON:MODule:INFormation?", '{"$type":"System.Collections.Generic.List`1[[TAU.Module.Channels.DI.DIModuleInfo, TAU.Module.Channels]], mscorlib","$values":[{"$type":"TAU.Module.Channels.DI.DIModuleInfo, TAU.Module.Channels","Index":0,"Category":0,"SN":"","HwVersion":"","SwVersion":"","TotalChannelCount":2,"Label":null,"ClassName":"DIModuleInfo"},{"$type":"TAU.Module.Channels.DI.DIModuleInfo, TAU.Module.Channels","Index":1,"Category":1,"SN":"6851022030037","HwVersion":"TAU-M1 V01.00.00.00","SwVersion":"TAU-M1 V01.05","TotalChannelCount":20,"Label":null,"ClassName":"DIModuleInfo"}]}'),
        ("MEASure:MODule:INFormation?", "0,,0,,,2,;1,6851022030037,1,TAU-M1 V01.00.00.00,TAU-M1 V01.05,20,"),
        ("MODule:INFormation?", "0,,0,,,2,;1,6851022030037,1,TAU-M1 V01.00.00.00,TAU-M1 V01.05,20,"),
    ],
)
def test_cmd(device, command, expected):
    """Test command execution functionality."""
    response = device.cmd(command)
    assert (
        response == expected
    ), f"Response should be '{expected}'"
