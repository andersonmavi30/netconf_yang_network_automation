#!/usr/bin/env python3

"""
NETCONF Connectivity Script
---------------------------
Establishes a NETCONF session to a Cisco IOS-XE device
and prints server capabilities.

Usage:
    python 01_netconf_connect.py --host 192.0.2.1 --username admin --password secret
    # or set NETCONF_HOST / NETCONF_USERNAME / NETCONF_PASSWORD env vars

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

import argparse
import logging

from netconf_client import get_connection

logger = logging.getLogger(__name__)


def netconf_connect(host, username, password):
    """
    Open a NETCONF session and print every server capability URI.

    The capability list tells us which YANG models and NETCONF features
    the device supports (e.g. candidate datastore, confirmed-commit, etc.).
    """
    with get_connection(host, username, password) as m:
        print("\n--- Server Capabilities ---")
        for capability in m.server_capabilities:
            print(capability)
        print(f"\nTotal capabilities: {len(list(m.server_capabilities))}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to a device via NETCONF and list its capabilities"
    )
    parser.add_argument("--host", default=None, help="Device IP/hostname (or set NETCONF_HOST)")
    parser.add_argument("--username", default=None, help="NETCONF username (or set NETCONF_USERNAME)")
    parser.add_argument("--password", default=None, help="NETCONF password (or set NETCONF_PASSWORD)")
    args = parser.parse_args()

    netconf_connect(args.host, args.username, args.password)
