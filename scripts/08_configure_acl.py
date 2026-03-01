#!/usr/bin/env python3

"""
NETCONF ACL Automation
-----------------------
Configures access control lists using YANG model.

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

from ncclient import manager


def configure_acl(host, username, password):
    """
    Applies ACL configuration.
    """

    acl_config = """
    <config>
        <!-- ACL configuration XML -->
    </config>
    """

    # NETCONF edit-config for ACL here


if __name__ == "__main__":
    configure_acl("192.0.2.1", "netconf_user", "netconf_password")