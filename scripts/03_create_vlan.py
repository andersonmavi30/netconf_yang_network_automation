#!/usr/bin/env python3

"""
NETCONF VLAN Provisioning
--------------------------
Creates a VLAN entry on a Cisco IOS-XE device using the
Cisco-IOS-XE-native YANG model and the NETCONF <edit-config> operation.

Usage:
    python 03_create_vlan.py --host 192.0.2.1 --username admin --password secret \
        --vlan-id 10 --vlan-name DEVNET_VLAN

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

import argparse
import logging

from netconf_client import get_connection

logger = logging.getLogger(__name__)


def create_vlan(host, username, password, vlan_id, vlan_name):
    """
    Provision a VLAN on the device via NETCONF <edit-config>.

    The payload targets the Cisco-IOS-XE-native namespace and follows the
    path: native → vlan → vlan-list → {id, name}.

    Parameters
    ----------
    vlan_id : int
        VLAN number (1-4094).
    vlan_name : str
        Descriptive VLAN name applied on the device.
    """
    # The config XML is built as an f-string so vlan_id and vlan_name are
    # injected at runtime. The Cisco-IOS-XE-native namespace is required
    # so the device maps the XML to the correct YANG model.
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

    with get_connection(host, username, password) as m:
        logger.info("Creating VLAN %s ('%s') on %s", vlan_id, vlan_name, host)

        # edit_config targets the 'running' datastore directly.
        # On devices with candidate datastore support, use target='candidate'
        # and follow with m.commit() – see 10_candidate_commit.py.
        response = m.edit_config(target="running", config=vlan_config)

        if response.ok:
            logger.info("VLAN %s created successfully", vlan_id)
        else:
            logger.warning("RPC errors: %s", response.errors)

        return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a VLAN via NETCONF")
    parser.add_argument("--host", default=None)
    parser.add_argument("--username", default=None)
    parser.add_argument("--password", default=None)
    parser.add_argument("--vlan-id", type=int, required=True, help="VLAN ID (1-4094)")
    parser.add_argument("--vlan-name", required=True, help="VLAN name")
    args = parser.parse_args()

    create_vlan(args.host, args.username, args.password, args.vlan_id, args.vlan_name)
