#!/usr/bin/env python3

"""
NETCONF Configuration Validation
---------------------------------
Demonstrates <validate> operation before commit.

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

from ncclient import manager


def validate_config(host, username, password):
    """
    Performs NETCONF <validate>.
    """

    # NETCONF validate operation here


if __name__ == "__main__":
    validate_config("192.0.2.1", "netconf_user", "netconf_password")