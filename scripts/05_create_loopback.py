#!/usr/bin/env python3

"""
NETCONF Loopback Interface Provisioning
----------------------------------------
Creates Loopback interface using ietf-interfaces model.

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

from ncclient import manager


def create_loopback(host, username, password, loopback_id, ip_address):
    """
    Creates Loopback interface configuration.
    """

    loopback_config = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback{loopback_id}</name>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                    ianaift:softwareLoopback
                </type>
                <enabled>true</enabled>
            </interface>
        </interfaces>
    </config>
    """

    # NETCONF edit-config logic here


if __name__ == "__main__":
    create_loopback("192.0.2.1", "netconf_user", "netconf_password", 99, "99.99.99.99")