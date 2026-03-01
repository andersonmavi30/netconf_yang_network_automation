# NETCONF + YANG Architecture Overview

Author: Anderson Martinez Virviescas  
Project: netconf_yang_network_automation

---

## 1. High-Level Architecture

This project follows a structured NETCONF automation workflow:

Python (ncclient)
        ↓
NETCONF (TCP 830 over SSH)
        ↓
Cisco IOS-XE Device
        ↓
YANG Models (Cisco Native / IETF / OpenConfig)

---

## 2. Key Components

- NETCONF client: Python + ncclient
- Data encoding: XML payloads
- Configuration datastore:
  - running
  - candidate
  - startup
- YANG models used:
  - Cisco-IOS-XE-native
  - ietf-interfaces
  - iana-if-type

---

## 3. Workflow Example

1. Establish NETCONF session
2. Lock datastore (optional)
3. Send <edit-config>
4. Validate configuration
5. Commit changes
6. Unlock datastore

---

## 4. Design Principles

- Infrastructure as Code mindset
- Separation of payload (XML) and logic (Python)
- Modular automation scripts
- Structured commit history