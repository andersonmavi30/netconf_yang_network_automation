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

netconf_yang_network_automation/
│
├── scripts/ → Python automation logic (ncclient)
├── configs/ → XML NETCONF payload examples
├── filters/ → Subtree filter examples for <get> operations
├── docs/ → Architecture and workflow documentation


---

## YANG Models Used

- Cisco-IOS-XE-native
- ietf-interfaces
- iana-if-type

---

## NETCONF Operations Demonstrated

- get
- edit-config
- validate
- commit
- candidate datastore workflow

---

## Design Principles

- Modular automation scripts
- Separation of logic and payload
- Version-controlled infrastructure
- Vendor model awareness
- Transactional configuration management

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

This project currently combines:

- **implemented examples** (for NETCONF connectivity and capability discovery), and
- **guided templates** (scripts intentionally prepared for future completion).

If you want to start contributing changes, check the initial review and roadmap:

- `docs/revision_inicial.md`

## Future Improvements

- OpenConfig model integration
- RESTCONF examples
- CI/CD validation pipeline
- Dockerized execution environment


## Use Cases Implemented

This lab includes structured examples for:

- NETCONF session establishment and capability discovery
- Interface operational state retrieval using subtree filters
- VLAN provisioning and removal via edit-config
- Loopback interface provisioning using ietf-interfaces
- OSPF process configuration
- SNMP configuration automation
- ACL provisioning using Cisco native model
- Configuration validation before commit
- Candidate datastore workflow and transactional commit