#!/usr/bin/env python3

"""
NETCONF Connectivity Script
---------------------------
Establishes a NETCONF session to a Cisco IOS-XE device
and retrieves server capabilities.

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

from ncclient import manager


def netconf_connect(host, username, password):
    """
    Establish NETCONF session and print server capabilities.
    """
    with manager.connect(
        host=host,
        port=830,
        username=username,
        password=password,
        hostkey_verify=False
    ) as m:
        print("NETCONF session established")
        for capability in m.server_capabilities:
            print(capability)


if __name__ == "__main__":
    HOST = "192.0.2.1"
    USERNAME = "netconf_user"
    PASSWORD = "netconf_password"

    netconf_connect(HOST, USERNAME, PASSWORD)