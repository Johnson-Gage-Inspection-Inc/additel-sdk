import pytest
from src.additel_sdk.system.communicate.wlan import WLAN
from conftest import use_wlan, use_wlan_fallback


@pytest.skip("Not important.", allow_module_level=True)
@pytest.fixture
def wlan_fixture(device) -> WLAN:
    return WLAN(device)


def test_set_state(wlan_fixture: WLAN):
    wlan_fixture.set_state(True)
    assert wlan_fixture.parent.command_log[-1] == \
        "SYSTem:COMMunicate:SOCKet:WLAN:STATe 1"
    wlan_fixture.set_state(False)
    assert wlan_fixture.parent.command_log[-1] == \
        "SYSTem:COMMunicate:SOCKet:WLAN:STATe 0"


def test_get_state_success(wlan_fixture: WLAN, use_wlan):
    if not use_wlan:
        wlan_fixture.parent.connection.responses[
            "SYSTem:COMMunicate:SOCKet:WLAN:STATe?"
        ] = "0"
        assert not wlan_fixture.get_state()
        wlan_fixture.parent.connection.responses[
            "SYSTem:COMMunicate:SOCKet:WLAN:STATe?"
        ] = "1"
    assert wlan_fixture.get_state()


@pytest.mark.skipif(use_wlan or use_wlan_fallback,
                    reason="Will succeed if WLAN is enabled")
def test_get_state_no_response(wlan_fixture: WLAN):
    wlan_fixture.parent.connection.responses[
        "SYSTem:COMMunicate:SOCKet:WLAN:STATe?"
    ] = None
    with pytest.raises(ValueError, match="No WiFi state information returned."):
        wlan_fixture.get_state()


@pytest.mark.skipif(use_wlan, reason="Will change device state")
def test_set_ip(wlan_fixture: WLAN):
    ip_address = "192.168.1.223"
    wlan_fixture.set_ip(ip_address)
    assert (
        wlan_fixture.parent.command_log[-1]
        == f"SYSTem:COMMunicate:SOCKet:WLAN:ADDRess {ip_address}"
    )


def test_get_ip_address_success(wlan_fixture: WLAN, use_wlan):
    ip_address = "192.168.1.223"
    if not use_wlan:
        wlan_fixture.parent.connection.responses[
            "SYSTem:COMMunicate:SOCKet:WLAN:ADDRess?"
        ] = ip_address
    assert wlan_fixture.get_ip_address() == ip_address


@pytest.mark.skipif(use_wlan or use_wlan_fallback,
                    reason="Will succeed if WLAN is enabled")
def test_get_ip_address_no_response(wlan_fixture: WLAN):
    wlan_fixture.parent.connection.responses[
        "SYSTem:COMMunicate:SOCKet:WLAN:ADDRess?"
    ] = None
    with pytest.raises(ValueError, match="No IP address information returned."):
        wlan_fixture.get_ip_address()


@pytest.mark.skipif(not use_wlan, reason="Will change device state")
def test_set_subnet_mask(wlan_fixture: WLAN):
    original = wlan_fixture.get_subnet_mask()
    subnet_mask = "255.255.255.0"
    wlan_fixture.set_subnet_mask(subnet_mask)
    success = subnet_mask == wlan_fixture.get_subnet_mask()
    wlan_fixture.set_subnet_mask(original)
    assert original == wlan_fixture.get_subnet_mask()
    assert success, "Subnet mask not set correctly."
    assert wlan_fixture.get_subnet_mask() == subnet_mask


def test_get_subnet_mask_success(wlan_fixture: WLAN):
    subnet_mask = "255.255.255.0"
    assert wlan_fixture.get_subnet_mask() == subnet_mask


@pytest.mark.skipif(use_wlan or use_wlan_fallback,
                    reason="Will succeed if WLAN is enabled")
def test_get_subnet_mask_no_response(wlan_fixture: WLAN):
    wlan_fixture.parent.connection.responses["SYSTem:COMMunicate:SOCKet:WLAN:MASK?"] = (
        None
    )
    with pytest.raises(ValueError, match="No subnet mask information returned."):
        wlan_fixture.get_subnet_mask()


@pytest.mark.skipif(not use_wlan, reason="Will change device state")
def test_set_gateway(wlan_fixture: WLAN):
    original = wlan_fixture.get_gateway()
    gateway = "192.168.1.1"
    wlan_fixture.set_gateway(gateway)
    success = gateway == wlan_fixture.get_gateway()
    wlan_fixture.set_gateway(original)
    assert original == wlan_fixture.get_gateway()
    assert success, "Gateway not set correctly."


def test_get_gateway_success(wlan_fixture: WLAN):
    gateway = "192.168.1.1"
    if not use_wlan:
        wlan_fixture.parent.connection.responses[
            "SYSTem:COMMunicate:SOCKet:WLAN:GATEway?"
        ] = gateway
    assert wlan_fixture.get_gateway() == gateway


@pytest.mark.skipif(use_wlan or use_wlan_fallback,
                    reason="Will succeed if WLAN is enabled")
def test_get_gateway_no_response(wlan_fixture: WLAN):
    wlan_fixture.parent.connection.responses[
        "SYSTem:COMMunicate:SOCKet:WLAN:GATEway?"
    ] = None
    with pytest.raises(ValueError, match="No gateway information returned."):
        wlan_fixture.get_gateway()


def test_get_mac_success(wlan_fixture: WLAN):
    mac_address = "00:11:22:33:44:55"
    wlan_fixture.parent.connection.responses["SYSTem:COMMunicate:SOCKet:WLAN:MAC?"] = (
        mac_address
    )
    assert wlan_fixture.get_mac() == mac_address


@pytest.mark.skipif(use_wlan or use_wlan_fallback,
                    reason="Will succeed if WLAN is enabled")
def test_get_mac_no_response(wlan_fixture: WLAN):
    wlan_fixture.parent.connection.responses["SYSTem:COMMunicate:SOCKet:WLAN:MAC?"] = (
        None
    )
    with pytest.raises(ValueError, match="No MAC address information returned."):
        wlan_fixture.get_mac()


def test_set_dhcp(wlan_fixture: WLAN):
    wlan_fixture.set_dhcp(True)
    assert wlan_fixture.parent.command_log[-1] == \
        "SYSTem:COMMunicate:SOCKet:WLAN:DHCP 1"
    wlan_fixture.set_dhcp(False)
    assert wlan_fixture.parent.command_log[-1] == \
        "SYSTem:COMMunicate:SOCKet:WLAN:DHCP 0"


def test_get_dhcp_success(wlan_fixture: WLAN):
    wlan_fixture.parent.connection.responses["SYSTem:COMMunicate:SOCKet:WLAN:DHCP?"] = (
        "1"
    )
    assert wlan_fixture.get_dhcp()

    wlan_fixture.parent.connection.responses["SYSTem:COMMunicate:SOCKet:WLAN:DHCP?"] = (
        "0"
    )
    assert wlan_fixture.get_dhcp()


@pytest.mark.skipif(use_wlan or use_wlan_fallback,
                    reason="Will succeed if WLAN is enabled")
def test_get_dhcp_no_response(wlan_fixture: WLAN):
    wlan_fixture.parent.connection.responses["SYSTem:COMMunicate:SOCKet:WLAN:DHCP?"] = (
        None
    )
    with pytest.raises(ValueError, match="No DHCP state information returned."):
        wlan_fixture.get_dhcp()


def test_set_ssid_success(wlan_fixture: WLAN):
    ssid = "MyWiFi"
    wlan_fixture.parent.send_command(f"SYSTem:COMMunicate:SOCKet:WLAN:SSID {ssid}")
    assert (
        wlan_fixture.parent.command_log[-1]
        == f"SYSTem:COMMunicate:SOCKet:WLAN:SSID {ssid}"
    )


@pytest.mark.skipif(use_wlan, reason="Would break WLAN connection")
def test_connect_with_password(wlan_fixture: WLAN):
    ssid = "MyWiFi"
    password = "password123"
    wlan_fixture.parent.send_command(
        f"SYSTem:COMMunicate:SOCKet:WLAN:CONNect {ssid},{password}"
    )
    assert (
        wlan_fixture.parent.command_log[-1]
        == f"SYSTem:COMMunicate:SOCKet:WLAN:CONNect {ssid},{password}"
    )


@pytest.mark.skipif(use_wlan or use_wlan_fallback,
                    reason="Would break WLAN connection")
def test_connect_without_password(wlan_fixture: WLAN):
    ssid = "MyWiFi"
    wlan_fixture.parent.send_command(f"SYSTem:COMMunicate:SOCKet:WLAN:CONNect {ssid}")
    assert (
        wlan_fixture.parent.command_log[-1]
        == f"SYSTem:COMMunicate:SOCKet:WLAN:CONNect {ssid}"
    )


def test_get_connection_success(wlan_fixture: WLAN):
    connection_status = "Connected"
    wlan_fixture.parent.connection.responses[
        "SYSTem:COMMunicate:SOCKet:WLAN:CONNect?"
    ] = connection_status
    assert wlan_fixture.get_connection() == connection_status


@pytest.mark.skipif(use_wlan or use_wlan_fallback,
                    reason="Will succeed if WLAN is enabled")
def test_get_connection_no_response(wlan_fixture: WLAN):
    wlan_fixture.parent.connection.responses[
        "SYSTem:COMMunicate:SOCKet:WLAN:CONNect?"
    ] = None
    with pytest.raises(ValueError, match="No connection information returned."):
        wlan_fixture.get_connection()


@pytest.mark.skipif(use_wlan, reason="Will change device state")
def test_disconnect(wlan_fixture: WLAN, use_wlan):
    wlan_fixture.disconnect()
    assert wlan_fixture.parent.command_log[-1] == \
        "SYSTem:COMMunicate:SOCKet:WLAN:DISConnect", "Disconnect command not sent."


def test_get_dbm_success(wlan_fixture: WLAN):
    dbm_value = "-50 dBm"
    wlan_fixture.parent.connection.responses["SYSTem:COMMunicate:SOCKet:WLAN:DBM?"] = (
        dbm_value
    )
    assert wlan_fixture.get_dbm() == dbm_value


@pytest.mark.skipif(use_wlan or use_wlan_fallback,
                    reason="Will succeed if WLAN is enabled")
def test_get_dbm_no_response(wlan_fixture: WLAN):
    wlan_fixture.parent.connection.responses["SYSTem:COMMunicate:SOCKet:WLAN:DBM?"] = (
        None
    )
    with pytest.raises(ValueError, match="No signal strength information returned."):
        wlan_fixture.get_dbm()
