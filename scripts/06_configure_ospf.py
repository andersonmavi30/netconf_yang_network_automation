#!/usr/bin/env python3

"""
NETCONF OSPF Configuration
---------------------------
Configures OSPF process using Cisco IOS-XE YANG model.

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

from ncclient import manager


def configure_ospf(host, username, password, process_id):
    """
    Configures OSPF process.
    """

    ospf_config = f"""
    <config>
        <!-- OSPF configuration XML would be defined here -->
    </config>
    """

    # NETCONF edit-config for OSPF here


if __name__ == "__main__":
    configure_ospf("192.0.2.1", "netconf_user", "netconf_password", 1)