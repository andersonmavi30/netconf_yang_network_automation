# Laboratorio de Automatización de Redes con NETCONF y YANG

🇺🇸 [English](README.md)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![NETCONF](https://img.shields.io/badge/Protocol-NETCONF-green)
![YANG](https://img.shields.io/badge/Model-YANG-orange)
![Cisco IOS-XE](https://img.shields.io/badge/Platform-Cisco_IOS--XE-red)
![Infrastructure as Code](https://img.shields.io/badge/Approach-Infrastructure_as_Code-purple)

Autor: Anderson Martinez Virviescas

---

## Descripción general

Este proyecto demuestra automatización estructurada de redes usando NETCONF y modelos YANG sobre dispositivos Cisco IOS-XE.

El repositorio incluye:

- Programabilidad basada en modelos
- Gestión de sesiones NETCONF
- Separación de payloads XML
- Filtros subtree
- Flujo con datastore candidate
- Principios de Infrastructure as Code

---

## Estructura del proyecto

```
netconf_yang_network_automation/
│
├── scripts/
│   ├── netconf_client.py       ← Módulo compartido de conexión (logging + manejo de errores)
│   ├── 01_netconf_connect.py   ← Establecimiento de sesión y descubrimiento de capabilities
│   ├── 02_get_interfaces.py    ← <get> con filtro subtree (ietf-interfaces)
│   ├── 03_create_vlan.py       ← Creación de VLAN con <edit-config>
│   ├── 04_delete_vlan.py       ← Eliminación de VLAN con <edit-config> (operation="delete")
│   ├── 05_create_loopback.py   ← Loopback con <edit-config> (ietf-interfaces)
│   ├── 06_configure_ospf.py    ← Proceso OSPF con <edit-config>
│   ├── 07_configure_snmp.py    ← Comunidad SNMP con <edit-config>
│   ├── 08_configure_acl.py     ← ACL extendida con <edit-config>
│   ├── 09_validate_config.py   ← <validate> sobre candidate
│   └── 10_candidate_commit.py  ← Flujo completo lock→edit→validate→commit→unlock
│
├── configs/                    ← Ejemplos independientes de payloads XML
├── filters/                    ← Ejemplos de filtros subtree para operaciones <get>
├── docs/                       ← Documentación de arquitectura y flujos
├── .env.example                ← Plantilla de credenciales (copiar a .env)
└── requirements.txt
```

---

## Inicio rápido

### 1. Instalar dependencias

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar credenciales

```bash
cp .env.example .env
# Edita .env con IP, usuario y contraseña del dispositivo
export $(cat .env | xargs)
```

También puedes pasar credenciales como argumentos CLI (consulta `--help` en cada script).

### 3. Ejecutar un script

```bash
# Listar capabilities del servidor
python scripts/01_netconf_connect.py --host 192.0.2.1 --username admin --password secret

# Obtener estado de interfaces
python scripts/02_get_interfaces.py --host 192.0.2.1 --username admin --password secret

# Crear VLAN 10
python scripts/03_create_vlan.py --host 192.0.2.1 --username admin --password secret \
    --vlan-id 10 --vlan-name DEVNET_VLAN

# Flujo transaccional completo (candidate → commit)
python scripts/10_candidate_commit.py --host 192.0.2.1 --username admin --password secret \
    --vlan-id 20 --vlan-name PROD_VLAN
```

---

## Modelos YANG utilizados

| Modelo | Namespace | Uso |
|---|---|---|
| Cisco-IOS-XE-native | `http://cisco.com/ns/yang/Cisco-IOS-XE-native` | VLANs, OSPF, SNMP, ACLs |
| ietf-interfaces | `urn:ietf:params:xml:ns:yang:ietf-interfaces` | Estado y configuración de interfaces |
| iana-if-type | `urn:ietf:params:xml:ns:yang:iana-if-type` | Definiciones de tipos de interfaz |

---

## Operaciones NETCONF demostradas

| Script | Operación | Datastore |
|---|---|---|
| 01 | Sesión + intercambio de capabilities | — |
| 02 | `<get>` con filtro subtree | operational |
| 03 | `<edit-config>` merge | running |
| 04 | `<edit-config>` delete | running |
| 05 | `<edit-config>` merge | running |
| 06 | `<edit-config>` merge | running |
| 07 | `<edit-config>` merge | running |
| 08 | `<edit-config>` merge | running |
| 09 | `<validate>` | candidate |
| 10 | lock → edit → validate → commit → unlock | candidate→running |

---

## Arquitectura

```
Scripts Python (ncclient)
        │
        │  SSH / TCP 830
        ▼
Agente NETCONF Cisco IOS-XE
        │
        │  Resolución de modelos YANG
        ▼
Datastores de configuración (running / candidate / startup)
```

Todos los scripts comparten un único módulo de conexión (`netconf_client.py`) que gestiona la sesión, el logging y la propagación de errores.

---

## Principios de diseño

- Scripts modulares: una responsabilidad por archivo
- Separación entre lógica y payload XML
- Módulo de conexión compartido para evitar duplicación
- Logging estructurado en cada script
- Argumentos CLI + variables de entorno para credenciales
- Seguridad transaccional mediante el datastore candidate

---

## Por qué importa

La automatización basada en modelos reduce:

- Parsing frágil de CLI
- Errores humanos de configuración
- Despliegues no repetibles

Y habilita:

- Automatización estructurada
- Integración CI/CD
- Aprovisionamiento escalable
- Flujos empresariales reproducibles

---

## Estado actual del repositorio

Los 10 scripts están implementados y listos para ejecutarse contra dispositivos Cisco IOS-XE con NETCONF habilitado, físicos, virtuales o DevNet Sandbox.

## Mejoras futuras

- Integración con modelos OpenConfig
- Ejemplos RESTCONF
- Pipeline de validación CI/CD
- Entorno de ejecución dockerizado
- Pruebas unitarias con sesiones ncclient simuladas
