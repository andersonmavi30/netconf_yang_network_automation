# NETCONF and YANG Network Automation Lab

![Python](https://img.shields.io/badge/Python-3.x-blue)
![NETCONF](https://img.shields.io/badge/Protocol-NETCONF-green)
![YANG](https://img.shields.io/badge/Model-YANG-orange)
![Cisco IOS-XE](https://img.shields.io/badge/Platform-Cisco_IOS--XE-red)
![Infrastructure as Code](https://img.shields.io/badge/Approach-Infrastructure_as_Code-purple)

Author: Anderson Martinez Virviescas

---

## Overview

This project demonstrates structured network automation using NETCONF and YANG models on Cisco IOS-XE devices.

The repository showcases:

- Model-driven programmability
- NETCONF session management
- XML payload separation
- Subtree filtering
- Candidate datastore workflow
- Infrastructure as Code principles

---

## Project Structure

```
netconf_yang_network_automation/
│
├── scripts/
│   ├── netconf_client.py       ← Shared connection module (logging + error handling)
│   ├── 01_netconf_connect.py   ← Session establishment & capability discovery
│   ├── 02_get_interfaces.py    ← <get> with subtree filter (ietf-interfaces)
│   ├── 03_create_vlan.py       ← <edit-config> VLAN creation
│   ├── 04_delete_vlan.py       ← <edit-config> VLAN removal (operation="delete")
│   ├── 05_create_loopback.py   ← <edit-config> Loopback (ietf-interfaces)
│   ├── 06_configure_ospf.py    ← <edit-config> OSPF process
│   ├── 07_configure_snmp.py    ← <edit-config> SNMP community
│   ├── 08_configure_acl.py     ← <edit-config> Extended ACL
│   ├── 09_validate_config.py   ← <validate> candidate datastore
│   └── 10_candidate_commit.py  ← Full lock→edit→validate→commit→unlock flow
│
├── configs/                    ← Standalone XML payload examples
├── filters/                    ← Subtree filter examples for <get> operations
├── docs/                       ← Architecture and workflow documentation
├── .env.example                ← Credential template (copy to .env)
└── requirements.txt
```

---

## Quick Start

### 1. Install dependencies

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure credentials

```bash
cp .env.example .env
# Edit .env with your device IP, username and password
export $(cat .env | xargs)
```

Or pass credentials as CLI arguments (see each script's `--help`).

### 3. Run a script

```bash
# List server capabilities
python scripts/01_netconf_connect.py --host 192.0.2.1 --username admin --password secret

# Retrieve interface state
python scripts/02_get_interfaces.py --host 192.0.2.1 --username admin --password secret

# Create VLAN 10
python scripts/03_create_vlan.py --host 192.0.2.1 --username admin --password secret \
    --vlan-id 10 --vlan-name DEVNET_VLAN

# Full transactional workflow (candidate → commit)
python scripts/10_candidate_commit.py --host 192.0.2.1 --username admin --password secret \
    --vlan-id 20 --vlan-name PROD_VLAN
```

---

## YANG Models Used

| Model | Namespace | Used for |
|---|---|---|
| Cisco-IOS-XE-native | `http://cisco.com/ns/yang/Cisco-IOS-XE-native` | VLANs, OSPF, SNMP, ACLs |
| ietf-interfaces | `urn:ietf:params:xml:ns:yang:ietf-interfaces` | Interface state & config |
| iana-if-type | `urn:ietf:params:xml:ns:yang:iana-if-type` | Interface type definitions |

---

## NETCONF Operations Demonstrated

| Script | Operation | Datastore |
|---|---|---|
| 01 | Session + capability exchange | — |
| 02 | `<get>` with subtree filter | operational |
| 03 | `<edit-config>` merge | running |
| 04 | `<edit-config>` delete | running |
| 05 | `<edit-config>` merge | running |
| 06 | `<edit-config>` merge | running |
| 07 | `<edit-config>` merge | running |
| 08 | `<edit-config>` merge | running |
| 09 | `<validate>` | candidate |
| 10 | lock → edit → validate → commit → unlock | candidate→running |

---

## Architecture

```
Python scripts (ncclient)
        │
        │  SSH / TCP 830
        ▼
Cisco IOS-XE NETCONF agent
        │
        │  YANG model resolution
        ▼
Configuration datastores (running / candidate / startup)
```

All scripts share a single connection module (`netconf_client.py`) that handles session setup, logging, and error propagation, keeping the individual automation scripts focused on their specific operation.

---

## Design Principles

- Modular automation scripts – one concern per file
- Separation of logic and XML payload
- Shared connection module eliminates code duplication
- Structured logging in every script
- CLI arguments + environment variable fallback for credentials
- Transactional safety via candidate datastore workflow

---

## Why This Matters

Model-driven automation eliminates:

- Fragile CLI parsing
- Human configuration errors
- Non-repeatable deployments

It enables:

- Structured automation
- CI/CD integration
- Scalable network provisioning
- Enterprise-ready workflows

---

## Current Repository Status

All 10 scripts are fully implemented and ready to run against a NETCONF-enabled Cisco IOS-XE device (physical, virtual, or DevNet sandbox).

## Future Improvements

- OpenConfig model integration
- RESTCONF examples
- CI/CD validation pipeline
- Dockerized execution environment
- Unit tests with mocked ncclient sessions
