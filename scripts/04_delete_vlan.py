#!/usr/bin/env python3

"""
NETCONF VLAN Removal
---------------------
Deletes VLAN configuration using <edit-config>.

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

from ncclient import manager


def delete_vlan(host, username, password, vlan_id):
    """
    Removes VLAN configuration via NETCONF.
    """

    vlan_delete_config = f"""
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <vlan operation="delete">
                <vlan-list>
                    <id>{vlan_id}</id>
                </vlan-list>
            </vlan>
        </native>
    </config>
    """

    # NETCONF <edit-config> delete operation here


if __name__ == "__main__":
    delete_vlan("192.0.2.1", "netconf_user", "netconf_password", 10)