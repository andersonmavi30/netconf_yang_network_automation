#!/usr/bin/env python3

"""
NETCONF Configuration Validation
---------------------------------
Demonstrates the NETCONF <validate> operation against the candidate
datastore before committing changes to the running configuration.

This is a safety check: the device verifies that the candidate config
is syntactically and semantically correct according to the YANG models
without actually applying it to the network.

Usage:
    python 09_validate_config.py --host 192.0.2.1 --username admin --password secret

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

import argparse
import logging

from netconf_client import get_connection

logger = logging.getLogger(__name__)


def validate_config(host, username, password):
    """
    Trigger a NETCONF <validate> RPC on the candidate datastore.

    The <validate> operation (RFC 6241 §8.6) checks that the contents of
    the specified datastore are valid according to all YANG constraints.
    A successful response means the config is safe to commit; an error
    means there is a conflict or constraint violation that must be resolved.

    Returns
    -------
    bool
        True if validation succeeded, False otherwise.
    """
    with get_connection(host, username, password) as m:
        logger.info("Validating candidate datastore on %s", host)

        # m.validate() sends the <validate> RPC targeting the candidate
        # datastore. This requires the device to support RFC 6241 §8.3
        # (candidate configuration capability).
        response = m.validate(source="candidate")

        if response.ok:
            logger.info("Candidate configuration is valid")
            return True
        else:
            logger.error("Validation failed: %s", response.errors)
            return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Validate the candidate datastore via NETCONF"
    )
    parser.add_argument("--host", default=None)
    parser.add_argument("--username", default=None)
    parser.add_argument("--password", default=None)
    args = parser.parse_args()

    result = validate_config(args.host, args.username, args.password)
    print("Validation result:", "PASSED" if result else "FAILED")
