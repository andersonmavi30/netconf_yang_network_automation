#!/usr/bin/env python3

"""
NETCONF VLAN Removal
---------------------
Deletes a VLAN from a Cisco IOS-XE device using the NETCONF
<edit-config> operation with operation="delete" attribute.

Usage:
    python 04_delete_vlan.py --host 192.0.2.1 --username admin --password secret \
        --vlan-id 10

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

import argparse
import logging

from netconf_client import get_connection

logger = logging.getLogger(__name__)


def delete_vlan(host, username, password, vlan_id):
    """
    Remove a VLAN from the device via NETCONF <edit-config>.

    The operation="delete" attribute instructs the NETCONF server to
    remove the matching node from the configuration datastore. If the
    node does not exist the server returns an rpc-error.

    Parameters
    ----------
    vlan_id : int
        VLAN number to delete.
    """
    # operation="delete" is a NETCONF edit operation attribute (RFC 6241 §7.2).
    # It tells the server to delete the element it is attached to.
    # Only <id> is needed to uniquely identify the vlan-list entry.
    vlan_delete_config = f"""
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <vlan>
                <vlan-list operation="delete">
                    <id>{vlan_id}</id>
                </vlan-list>
            </vlan>
        </native>
    </config>
    """

    with get_connection(host, username, password) as m:
        logger.info("Deleting VLAN %s from %s", vlan_id, host)

        response = m.edit_config(target="running", config=vlan_delete_config)

        if response.ok:
            logger.info("VLAN %s deleted successfully", vlan_id)
        else:
            logger.warning("RPC errors: %s", response.errors)

        return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete a VLAN via NETCONF")
    parser.add_argument("--host", default=None)
    parser.add_argument("--username", default=None)
    parser.add_argument("--password", default=None)
    parser.add_argument("--vlan-id", type=int, required=True, help="VLAN ID to remove")
    args = parser.parse_args()

    delete_vlan(args.host, args.username, args.password, args.vlan_id)
