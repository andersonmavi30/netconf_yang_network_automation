#!/usr/bin/env python3

"""
Shared NETCONF Client Module
-----------------------------
Provides a reusable context manager for NETCONF sessions with
logging and error handling consumed by all automation scripts.

Usage:
    from netconf_client import get_connection

    with get_connection(host, username, password) as m:
        response = m.get(...)

Credentials can also be loaded from environment variables:
    NETCONF_HOST, NETCONF_USERNAME, NETCONF_PASSWORD

Author: Anderson Martinez Virviescas
Project: netconf_yang_network_automation
"""

import logging
import os
from contextlib import contextmanager

from ncclient import manager

# ---------------------------------------------------------------------------
# Logging – all scripts inherit this configuration when they import this module
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

NETCONF_PORT = 830


@contextmanager
def get_connection(host=None, username=None, password=None, port=NETCONF_PORT):
    """
    Context manager that opens a NETCONF session and yields the manager object.

    Parameters
    ----------
    host : str, optional
        Device hostname or IP address. Falls back to NETCONF_HOST env var.
    username : str, optional
        NETCONF username. Falls back to NETCONF_USERNAME env var.
    password : str, optional
        NETCONF password. Falls back to NETCONF_PASSWORD env var.
    port : int
        NETCONF port (default 830).

    Yields
    ------
    ncclient.manager.Manager
        Active NETCONF session object.

    Raises
    ------
    ValueError
        If any required credential is missing.
    Exception
        Re-raises any ncclient transport or RPC error after logging it.
    """
    # Resolve credentials: explicit arguments take priority over env vars
    host = host or os.environ.get("NETCONF_HOST")
    username = username or os.environ.get("NETCONF_USERNAME")
    password = password or os.environ.get("NETCONF_PASSWORD")

    if not all([host, username, password]):
        raise ValueError(
            "Missing credentials. Pass host/username/password as arguments "
            "or set NETCONF_HOST, NETCONF_USERNAME, NETCONF_PASSWORD env vars."
        )

    logger.info("Connecting to %s:%s as '%s'", host, port, username)
    try:
        with manager.connect(
            host=host,
            port=port,
            username=username,
            password=password,
            hostkey_verify=False,          # Set True in production with known_hosts
            device_params={"name": "iosxe"},  # Enables IOS-XE specific behaviour
        ) as m:
            logger.info(
                "NETCONF session established (session-id: %s)", m.session_id
            )
            yield m
            logger.info("NETCONF session closed for %s", host)
    except Exception as exc:
        logger.error("NETCONF error on %s: %s", host, exc)
        raise
