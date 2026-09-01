# Cisco Routing & Switching — command reference

Read-only diagnostic commands first per platform-playbooks.md guardrails. Treat `clear`, `debug`, `write`, `copy running-config startup-config`, and any `config t` entry as state-changing — authorize before running.

## Interface and physical layer

- `show interface [type slot/port]` — status, errors, drops, duplex/speed, load, CRC/input/output errors.
- `show interface status` — condensed port status table, VLAN, duplex, speed across all ports (switch).
- `show interface counters errors` — isolate error counters without full interface dump.
- `show interface transceiver` / `show interface transceiver detail` — SFP/optic diagnostics (Tx/Rx power, temp).
- `show controllers ethernet-controller [int]` — PHY-level counters when `show interface` errors are ambiguous.
- `show cdp neighbors detail` / `show lldp neighbors detail` — verify physical topology and remote port ID match design.

## VLAN and L2

- `show vlan brief` — VLAN-to-port mapping.
- `show interfaces trunk` — trunk state, native VLAN, allowed VLANs, pruned VLANs.
- `show spanning-tree` / `show spanning-tree vlan [id]` — root bridge, port roles/states, detect STP loops or blocking.
- `show spanning-tree inconsistentports` — detect BPDU guard/loop guard triggered ports.
- `show mac address-table` / `show mac address-table dynamic interface [int]` — endpoint-to-port mapping, detect MAC flapping.
- `show etherchannel summary` — port-channel member status and bundling state.
- `show interfaces [int] switchport` — access/trunk mode, native VLAN, operational state per port.

## Layer 3 / routing

- `show ip interface brief` — quick up/down and IP assignment view.
- `show ip route` / `show ip route [prefix]` — RIB, confirm expected next-hop and source protocol.
- `show ip protocols` — active routing protocols and their timers/filters.
- `show ip cef` / `show ip cef [prefix] detail` — CEF forwarding table, confirm FIB matches RIB.
- `show adjacency detail` — L2 rewrite info per CEF adjacency; a route can be correct with a broken adjacency.

## OSPF

- `show ip ospf neighbor` — adjacency state (should be FULL); stuck in EXSTART/2WAY indicates MTU mismatch or DR/BDR issue.
- `show ip ospf interface [int]` — area, cost, timers, network type mismatch check.
- `show ip ospf database` — LSDB contents; compare across neighbors for sync issues.
- `debug ip ospf adj` (authorize first) — real-time adjacency formation troubleshooting.

## EIGRP

- `show ip eigrp neighbors` — adjacency and hold time.
- `show ip eigrp topology` / `show ip eigrp topology [prefix]` — successor/feasible successor, stuck-in-active detection.
- `show ip eigrp interfaces detail` — per-interface timers and authentication state.

## BGP

- `show ip bgp summary` — peer state, prefix counts; state other than "Established" is the first triage point.
- `show ip bgp neighbors [ip]` — capabilities, timers, last error/reset reason.
- `show ip bgp [prefix]` — path selection, AS-path, best-path reasoning.
- `show ip bgp neighbors [ip] advertised-routes` / `received-routes` — confirm what's actually exchanged vs expected.
- `show ip bgp neighbors [ip] routes` — routes accepted after inbound policy.

## Multicast

- `show ip mroute` — multicast routing table, incoming/outgoing interface list.
- `show ip pim neighbor` — PIM adjacency.
- `show ip igmp groups` — receiver join state on the local segment.

## HSRP/VRRP/GLBP

- `show standby brief` — HSRP group state, active/standby role.
- `show vrrp brief` — VRRP group state.
- `show glbp brief` — GLBP forwarder state.

## ACLs and QoS

- `show access-lists [name]` — hit counters per ACE, confirms which line is matching traffic.
- `show ip access-lists interface [int]` — applied ACLs per interface/direction.
- `show policy-map interface [int]` — QoS policy hit counters, drops per class.
- `show mls qos interface [int]` — trust boundary and queue mapping (switch).

## NAT (IOS)

- `show ip nat translations` — active translation table.
- `show ip nat statistics` — hits, misses, active translations count.

## Reachability tests (safe, read-generating)

- `ping [target] source [interface]` — verify from the correct source interface, not just default.
- `traceroute [target]` — hop-by-hop path; compare against expected topology.
- `ping [target] size [bytes] df-bit` — MTU/fragmentation testing.

## Logging and events

- `show logging` — local buffer; filter for interface flaps, ACL denies, routing adjacency changes.
- `show archive log config all` — configuration change history if archive logging is enabled.

## Correlation notes

- Always confirm CEF/adjacency state before concluding a "routing" problem — a correct RIB entry with a broken adjacency drops traffic silently.
- For STP-suspected loops, correlate `show spanning-tree` topology change count with the reported outage window before concluding STP is the cause.
- BGP/OSPF neighbor flaps: check interface error counters and CDP/LLDP neighbor stability first — L1/L2 instability is a common false "routing protocol" root cause.
