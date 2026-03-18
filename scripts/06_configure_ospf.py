#!/usr/bin/env python3

"""
NETCONF OSPF Configuration
---------------------------
Configures an OSPF process on a Cisco IOS-XE device using the
Cisco-IOS-XE-native YANG model and NETCONF <edit-config>.

Usage:
    python 06_configure_ospf.py --host 192.0.2.1 --username admin --password secret \
        --process-id 1 --router-id 1.1.1.1

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

import argparse
import logging

from netconf_client import get_connection

logger = logging.getLogger(__name__)


def configure_ospf(host, username, password, process_id, router_id="0.0.0.0"):
    """
    Push OSPF process configuration to the device via NETCONF.

    The payload uses the Cisco-IOS-XE-native namespace, following the
    path: native → router → ospf → {id, router-id}.

    Parameters
    ----------
    process_id : int
        OSPF process number (1-65535).
    router_id : str
        Router-ID in dotted-decimal notation (e.g. "1.1.1.1").
    """
    # The <ospf> element lives under <router> in the IOS-XE native model.
    # <id> is the OSPF process number; <router-id> sets the stable RID used
    # for adjacencies and LSA origination.
    ospf_config = f"""
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <router>
                <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                    <id>{process_id}</id>
                    <router-id>{router_id}</router-id>
                </ospf>
            </router>
        </native>
    </config>
    """

    with get_connection(host, username, password) as m:
        logger.info(
            "Configuring OSPF process %s (router-id %s) on %s",
            process_id, router_id, host,
        )

        response = m.edit_config(target="running", config=ospf_config)

        if response.ok:
            logger.info("OSPF process %s configured successfully", process_id)
        else:
            logger.warning("RPC errors: %s", response.errors)

        return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure OSPF via NETCONF")
    parser.add_argument("--host", default=None)
    parser.add_argument("--username", default=None)
    parser.add_argument("--password", default=None)
    parser.add_argument("--process-id", type=int, required=True, help="OSPF process ID")
    parser.add_argument("--router-id", default="0.0.0.0", help="OSPF router-id (e.g. 1.1.1.1)")
    args = parser.parse_args()

    configure_ospf(args.host, args.username, args.password, args.process_id, args.router_id)
