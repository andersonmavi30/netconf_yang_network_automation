#!/usr/bin/env python3

"""
NETCONF VLAN Provisioning
--------------------------
Creates VLAN configuration using <edit-config>.

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

from ncclient import manager


def create_vlan(host, username, password, vlan_id, vlan_name):
    """
    Sends VLAN configuration via NETCONF.
    """

    vlan_config = f"""
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <vlan>
                <vlan-list>
                    <id>{vlan_id}</id>
                    <name>{vlan_name}</name>
                </vlan-list>
            </vlan>
        </native>
    </config>
    """

    # NETCONF <edit-config> would be applied here


if __name__ == "__main__":
    create_vlan("192.0.2.1", "netconf_user", "netconf_password", 10, "DEVNET_VLAN")