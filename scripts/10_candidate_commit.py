#!/usr/bin/env python3

"""
NETCONF Candidate Configuration and Commit
-------------------------------------------
Demonstrates the full transactional workflow using the candidate datastore:
  1. Lock the candidate datastore (prevent concurrent edits)
  2. Apply configuration changes to the candidate (not yet active)
  3. Validate the candidate (YANG constraint check)
  4. Commit – copy candidate → running (activates the change)
  5. Unlock the candidate datastore

This is the recommended production pattern for NETCONF configuration because
it provides atomicity and rollback safety.

Usage:
    python 10_candidate_commit.py --host 192.0.2.1 --username admin --password secret \
        --vlan-id 20 --vlan-name PROD_VLAN

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

import argparse
import logging

from netconf_client import get_connection

logger = logging.getLogger(__name__)


def candidate_commit(host, username, password, vlan_id=20, vlan_name="PROD_VLAN"):
    """
    Apply a VLAN configuration using the full candidate datastore workflow.

    This function is intentionally simple (one VLAN) to keep the focus on
    the transactional pattern.  In real use, edit_config can push any
    payload to the candidate before committing.

    Parameters
    ----------
    vlan_id : int
        VLAN to create as part of the demonstration.
    vlan_name : str
        Name for the demo VLAN.

    Returns
    -------
    bool
        True if the commit succeeded, False otherwise.
    """
    vlan_config = f"""
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <vlan>
                <vlan-list>
                    <id>{vlan_id}</id>
                    <name>{vlan_name}</name>
                </vlan-list>
            </vlan>
        </native>
    </config>
    """

    with get_connection(host, username, password) as m:
        # -----------------------------------------------------------------
        # Step 1: Lock the candidate datastore
        # Prevents other NETCONF sessions from modifying the candidate
        # concurrently, ensuring our changes are applied atomically.
        # -----------------------------------------------------------------
        logger.info("Locking candidate datastore on %s", host)
        m.lock(target="candidate")

        try:
            # -------------------------------------------------------------
            # Step 2: Edit-config on candidate (changes are NOT active yet)
            # The running configuration is untouched at this point.
            # -------------------------------------------------------------
            logger.info("Applying VLAN %s config to candidate datastore", vlan_id)
            m.edit_config(target="candidate", config=vlan_config)

            # -------------------------------------------------------------
            # Step 3: Validate the candidate datastore
            # Device checks YANG constraints and model consistency before
            # any changes reach the running configuration.
            # -------------------------------------------------------------
            logger.info("Validating candidate configuration")
            validate_response = m.validate(source="candidate")

            if not validate_response.ok:
                logger.error("Validation failed: %s", validate_response.errors)
                logger.warning("Rolling back – discarding candidate changes")
                m.discard_changes()
                return False

            # -------------------------------------------------------------
            # Step 4: Commit – atomically copies candidate → running
            # The change becomes active on the device only at this point.
            # -------------------------------------------------------------
            logger.info("Committing candidate configuration to running")
            commit_response = m.commit()

            if commit_response.ok:
                logger.info(
                    "Commit successful: VLAN %s ('%s') is now active", vlan_id, vlan_name
                )
                return True
            else:
                logger.error("Commit failed: %s", commit_response.errors)
                return False

        except Exception as exc:
            # Discard any uncommitted candidate changes on unexpected errors
            logger.error("Unexpected error, discarding candidate changes: %s", exc)
            m.discard_changes()
            raise

        finally:
            # -----------------------------------------------------------------
            # Step 5: Always unlock the candidate datastore
            # The finally block ensures the lock is released even if an
            # exception occurs, preventing deadlocks for other sessions.
            # -----------------------------------------------------------------
            logger.info("Unlocking candidate datastore")
            m.unlock(target="candidate")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Demonstrate the full NETCONF candidate/commit workflow"
    )
    parser.add_argument("--host", default=None)
    parser.add_argument("--username", default=None)
    parser.add_argument("--password", default=None)
    parser.add_argument("--vlan-id", type=int, default=20, help="Demo VLAN ID")
    parser.add_argument("--vlan-name", default="PROD_VLAN", help="Demo VLAN name")
    args = parser.parse_args()

    success = candidate_commit(
        args.host, args.username, args.password, args.vlan_id, args.vlan_name
    )
    print("Workflow result:", "SUCCESS" if success else "FAILED")
