#!/usr/bin/env python3

"""
NETCONF Loopback Interface Provisioning
----------------------------------------
Creates a Loopback interface using the vendor-neutral ietf-interfaces
YANG model (RFC 8343) and the NETCONF <edit-config> operation.

Usage:
    python 05_create_loopback.py --host 192.0.2.1 --username admin --password secret \
        --loopback-id 99 --ip-address 99.99.99.99

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

import argparse
import logging

from netconf_client import get_connection

logger = logging.getLogger(__name__)


def create_loopback(host, username, password, loopback_id, ip_address):
    """
    Provision a Loopback interface via NETCONF using ietf-interfaces.

    The ietf-interfaces model is vendor-neutral (IETF RFC 8343) so the
    same payload works across vendors that support it.  The interface type
    is declared using the iana-if-type namespace (RFC 7224).

    Parameters
    ----------
    loopback_id : int
        Loopback interface number (e.g. 99 → Loopback99).
    ip_address : str
        IPv4 address to assign (informational – full IP config requires
        the ietf-ip augmentation which can be added here as needed).
    """
    # ianaift:softwareLoopback is the IANA-registered type for loopback
    # interfaces. The namespace prefix must be declared in the same element
    # that uses it (xmlns:ianaift="...") for XML correctness.
    loopback_config = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback{loopback_id}</name>
                <description>Loopback {loopback_id} - {ip_address}</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                    ianaift:softwareLoopback
                </type>
                <enabled>true</enabled>
            </interface>
        </interfaces>
    </config>
    """

    with get_connection(host, username, password) as m:
        logger.info("Creating Loopback%s (%s) on %s", loopback_id, ip_address, host)

        response = m.edit_config(target="running", config=loopback_config)

        if response.ok:
            logger.info("Loopback%s created successfully", loopback_id)
        else:
            logger.warning("RPC errors: %s", response.errors)

        return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Loopback interface via NETCONF")
    parser.add_argument("--host", default=None)
    parser.add_argument("--username", default=None)
    parser.add_argument("--password", default=None)
    parser.add_argument("--loopback-id", type=int, required=True, help="Loopback number")
    parser.add_argument("--ip-address", required=True, help="IPv4 address (informational)")
    args = parser.parse_args()

    create_loopback(args.host, args.username, args.password, args.loopback_id, args.ip_address)
