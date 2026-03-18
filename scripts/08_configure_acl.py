#!/usr/bin/env python3

"""
NETCONF ACL Automation
-----------------------
Configures an extended IP access control list on a Cisco IOS-XE device
using the Cisco-IOS-XE-native YANG model and NETCONF <edit-config>.

Usage:
    python 08_configure_acl.py --host 192.0.2.1 --username admin --password secret \
        --acl-name DEVNET_ACL

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

import argparse
import logging

from netconf_client import get_connection

logger = logging.getLogger(__name__)


def configure_acl(host, username, password, acl_name="DEVNET_ACL"):
    """
    Push an extended ACL configuration to the device via NETCONF.

    The payload creates a named extended ACL with a single permissive
    entry (sequence 10: permit ip any any) as a baseline demonstration.
    Adjust <permit> entries to match your security policy before applying
    this in any production environment.

    YANG path: native → ip → access-list → extended → {name, access-list-seq-rule}

    Parameters
    ----------
    acl_name : str
        Name for the extended ACL (alphanumeric, no spaces).
    """
    # <sequence> is the ACE (Access Control Entry) sequence number.
    # <permit> defines the action; nested elements specify the protocol
    # and source/destination address matchers (<any/> matches all addresses).
    acl_config = f"""
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <ip>
                <access-list>
                    <extended>
                        <name>{acl_name}</name>
                        <access-list-seq-rule>
                            <sequence>10</sequence>
                            <permit>
                                <protocol>ip</protocol>
                                <any/>
                                <any/>
                            </permit>
                        </access-list-seq-rule>
                    </extended>
                </access-list>
            </ip>
        </native>
    </config>
    """

    with get_connection(host, username, password) as m:
        logger.info("Configuring ACL '%s' on %s", acl_name, host)

        response = m.edit_config(target="running", config=acl_config)

        if response.ok:
            logger.info("ACL '%s' configured successfully", acl_name)
        else:
            logger.warning("RPC errors: %s", response.errors)

        return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure an extended ACL via NETCONF")
    parser.add_argument("--host", default=None)
    parser.add_argument("--username", default=None)
    parser.add_argument("--password", default=None)
    parser.add_argument("--acl-name", default="DEVNET_ACL", help="Extended ACL name")
    args = parser.parse_args()

    configure_acl(args.host, args.username, args.password, args.acl_name)
