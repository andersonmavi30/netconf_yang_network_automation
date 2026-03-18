#!/usr/bin/env python3

"""
NETCONF Interface State Retrieval
----------------------------------
Retrieves interface operational data using the NETCONF <get> operation
with a subtree filter scoped to the ietf-interfaces YANG model.

Usage:
    python 02_get_interfaces.py --host 192.0.2.1 --username admin --password secret

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

import argparse
import logging

from netconf_client import get_connection

logger = logging.getLogger(__name__)


def get_interfaces(host, username, password):
    """
    Retrieve interface data from the device using NETCONF <get>.

    The subtree filter limits the response to the ietf-interfaces branch
    only, avoiding retrieval of the entire device configuration/state tree.

    Returns
    -------
    str
        Raw XML string with the interface data returned by the device.
    """
    # Subtree filter: only retrieve the <interfaces> subtree from the
    # ietf-interfaces namespace (RFC 8343). This avoids fetching the whole
    # device state tree, which can be very large on production devices.
    interface_filter = """
    <filter>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
    </filter>
    """

    with get_connection(host, username, password) as m:
        logger.info("Sending <get> with ietf-interfaces subtree filter")

        # m.get() sends a NETCONF <get> RPC.
        # The filter tuple ("subtree", xml_string) tells ncclient to use
        # subtree filtering (as opposed to XPath filtering).
        response = m.get(filter=("subtree", interface_filter))

        logger.info("Interface data retrieved successfully")
        print(response)
        return str(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve interface state via NETCONF")
    parser.add_argument("--host", default=None, help="Device IP/hostname")
    parser.add_argument("--username", default=None, help="NETCONF username")
    parser.add_argument("--password", default=None, help="NETCONF password")
    args = parser.parse_args()

    get_interfaces(args.host, args.username, args.password)
