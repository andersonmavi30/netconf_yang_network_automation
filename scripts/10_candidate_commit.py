#!/usr/bin/env python3

"""
NETCONF Candidate Configuration and Commit
-------------------------------------------
Demonstrates candidate datastore workflow.

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

from ncclient import manager


def candidate_commit(host, username, password):
    """
    Uses candidate datastore and commit.
    """

    # lock candidate
    # edit-config candidate
    # validate
    # commit


if __name__ == "__main__":
    candidate_commit("192.0.2.1", "netconf_user", "netconf_password")