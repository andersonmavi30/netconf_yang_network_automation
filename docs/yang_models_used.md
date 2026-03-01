# YANG Models Used in This Project

Author: Anderson Martinez Virviescas  
Project: netconf_yang_network_automation

---

## 1. Cisco-IOS-XE-native

Namespace:
http://cisco.com/ns/yang/Cisco-IOS-XE-native

Used for:
- VLAN configuration
- OSPF configuration
- SNMP configuration
- ACL configuration

This model represents Cisco CLI structure mapped into YANG hierarchy.

---

## 2. IETF Interfaces Model

Namespace:
urn:ietf:params:xml:ns:yang:ietf-interfaces

Used for:
- Loopback interface provisioning
- Interface state retrieval

Vendor-neutral model supported across multiple platforms.

---

## 3. IANA Interface Types

Namespace:
urn:ietf:params:xml:ns:yang:iana-if-type

Used for:
- Defining interface types (softwareLoopback, ethernetCsmacd, etc.)

---

## 4. Datastore Models

This project demonstrates usage of:

- running datastore
- candidate datastore
- configuration validation

---

## 5. Why YANG?

YANG provides:

- Structured configuration
- Validation capability
- Model-driven programmability
- Reduced dependency on CLI parsing
- Better integration with CI/CD workflows