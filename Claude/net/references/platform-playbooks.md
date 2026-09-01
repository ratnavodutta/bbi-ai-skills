# Platform playbooks

Use this to select diagnostic domains, not assume syntax. Confirm version, context, and authorization.

## Guardrails

Prefer show/get/list/query/test. Display target/context first. Bound logs and captures. Treat create/update/delete, commit/apply, clear/reset, reload/restart, failover, detach, route/policy changes, and production captures as state-changing or disruptive; obtain explicit authorization immediately before execution. Record actual commands/output; never synthesize results.

## Azure CLI

Validate subscription/tenant/region; inspect effective routes/NSGs, Network Watcher, route tables, Firewall, VPN/ExpressRoute, load balancers, Private Endpoint/DNS, and vWAN. Correlate configuration with logs/flows.

## AWS CLI

Validate account, role/profile/region; inspect ENIs, routes, security groups, NACLs, TGW, peering, VPN/Direct Connect, target health, Route 53, Reachability Analyzer, Network Firewall, and Flow Logs.

## Cisco ASR, ASA, and FTD

Inspect interfaces, routes/VRFs, adjacency/CEF, BGP/OSPF, ACL hits, NAT, VPN SAs, connections, drops, HA, and targeted captures. Account for FMC deployment state on FTD. Do not clear state unless authorized.

## Cisco ACI

Inspect APIC faults/events/audit, endpoints, EPG/BD/VRF, contracts/zoning, COOP, fabric routes, TEP reachability, interfaces, L3Out, and leaf forwarding. Map endpoints to leaves first.

## Citrix NetScaler

Inspect vServers, services/groups, monitors, bindings, persistence, SSL, SNIP/MIP/VIP, routes, HA, policy hits, counters, and bounded traces. Separate frontend from backend health.

## Meraki

Inspect organization/network, devices, uplinks, VLAN/routes, VPN, firewall, events, clients, ports, and bounded Dashboard/API captures. Treat firmware/template changes as high-impact.

## Palo Alto Networks

Inspect virtual routers/routes, zones, policy hits, sessions, NAT, VPN, logs, HA, interfaces, and capture stages. Commits require authorization.

## FortiGate

Inspect VDOM, interfaces/routes, policy lookup, sessions, NAT, IPsec, SD-WAN, HA, logs, debug flow, and sniffer evidence. Bound and disable debugging after collection.

## Correlation

Normalize timestamps, compare the same five-tuple per hop, track pre/post-NAT identities, and test MTU/MSS, asymmetry, overlaps, split DNS, and stateful sessions where relevant.
