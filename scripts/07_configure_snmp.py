#!/usr/bin/env python3

"""
NETCONF SNMP Configuration
---------------------------
Configures an SNMP read-only community string on a Cisco IOS-XE device
using the Cisco-IOS-XE-native YANG model.

Usage:
    python 07_configure_snmp.py --host 192.0.2.1 --username admin --password secret \
        --community DEVNET_COMMUNITY

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

import argparse
import logging

from netconf_client import get_connection

logger = logging.getLogger(__name__)


def configure_snmp(host, username, password, community="DEVNET_COMMUNITY"):
    """
    Apply an SNMP read-only community via NETCONF <edit-config>.

    The payload targets: native → snmp-server → community → {name, ro}.
    The <ro/> empty element signals read-only access; replace with <rw/>
    for read-write (exercise caution in production environments).

    Parameters
    ----------
    community : str
        SNMP community string to configure.
    """
    # <ro/> is an empty element (boolean-style leaf in the YANG model)
    # that sets the community permission to read-only.
    snmp_config = f"""
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <snmp-server>
                <community>
                    <name>{community}</name>
                    <ro/>
                </community>
            </snmp-server>
        </native>
    </config>
    """

    with get_connection(host, username, password) as m:
        logger.info("Configuring SNMP community '%s' (ro) on %s", community, host)

        response = m.edit_config(target="running", config=snmp_config)

        if response.ok:
            logger.info("SNMP community '%s' configured successfully", community)
        else:
            logger.warning("RPC errors: %s", response.errors)

        return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure SNMP community via NETCONF")
    parser.add_argument("--host", default=None)
    parser.add_argument("--username", default=None)
    parser.add_argument("--password", default=None)
    parser.add_argument(
        "--community", default="DEVNET_COMMUNITY", help="SNMP community string"
    )
    args = parser.parse_args()

    configure_snmp(args.host, args.username, args.password, args.community)
