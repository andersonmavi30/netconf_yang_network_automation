# NETCONF Operational Workflow

Author: Anderson Martinez Virviescas  
Project: netconf_yang_network_automation

---

## 1. Session Establishment

NETCONF operates over SSH (TCP port 830).

Steps:
1. SSH transport negotiation
2. Capability exchange
3. Session ID assignment

---

## 2. Core Operations Used

This project demonstrates:

- <get>
- <edit-config>
- <validate>
- <commit>
- candidate datastore workflow

---

## 3. Typical Configuration Flow

Example sequence:

1. Lock candidate datastore
2. Send <edit-config> with XML payload
3. Validate configuration
4. Commit changes
5. Unlock datastore

This ensures transactional consistency.

---

## 4. Filtering Strategy

Subtree filters are used to:

- Retrieve specific interfaces
- Query VLAN information
- Reduce unnecessary data retrieval

---

## 5. Error Handling Concept

Production-ready automation should include:

- RPC error handling
- Validation checks
- Rollback strategy
- Logging mechanisms

---

## 6. Infrastructure as Code Perspective

NETCONF + YANG enables:

- Declarative configuration
- Repeatable deployments
- CI/CD integration
- Vendor abstraction (when using standard models)