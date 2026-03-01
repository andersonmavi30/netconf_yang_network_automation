#!/usr/bin/env python3

"""
NETCONF Interface State Retrieval
----------------------------------
Retrieves interface operational data using <get> operation.

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

from ncclient import manager


def get_interfaces(host, username, password):
    """
    Retrieves interface information using subtree filter.
    """

    interface_filter = """
    <filter>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
    </filter>
    """

    # NETCONF <get> operation would be performed here


if __name__ == "__main__":
    HOST = "192.0.2.1"
    USERNAME = "netconf_user"
    PASSWORD = "netconf_password"

    get_interfaces(HOST, USERNAME, PASSWORD)