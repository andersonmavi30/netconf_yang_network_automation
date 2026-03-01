#!/usr/bin/env python3

"""
NETCONF SNMP Configuration
----------------------------
Configures SNMP settings via YANG model.

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

from ncclient import manager


def configure_snmp(host, username, password):
    """
    Applies SNMP configuration using NETCONF.
    """

    snmp_config = """
    <config>
        <!-- SNMP configuration XML -->
    </config>
    """

    # NETCONF edit-config for SNMP here


if __name__ == "__main__":
    configure_snmp("192.0.2.1", "netconf_user", "netconf_password")