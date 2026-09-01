# Citrix NetScaler (ADC) — command reference

CLI shown (`nscli` / shell); GUI equivalents exist under Traffic Management and Reporting. Read-only `show`/`stat` commands first. `set`, `enable`/`disable server|service`, `save config`, and HA `force failover` require explicit authorization.

## System and HA state

- `show ns hardware` / `show version` — platform and build info.
- `show ns cpu` / `show ns memory` — resource state check before deeper diagnosis.
- `show ha node` — HA role (primary/secondary), sync and propagation status.
- `show ha calloutstats` — HA heartbeat/health check stats when suspecting split-brain or failover flapping.

## Interfaces and networking

- `show interface` — port status, errors, speed/duplex.
- `show vlan` — VLAN-to-interface bindings.
- `show ip` — configured IP addresses (NSIP, SNIPs, VIPs) and their roles.
- `show route` — RIB.
- `show arp` — ARP table, useful for confirming L2 reachability to backend servers.

## Load balancing — vServers

- `show lb vserver` — all LB vServers with state (UP/DOWN/OUT OF SERVICE).
- `show lb vserver [name]` — detailed state, bound services, persistence, method.
- `show service` / `show service [name]` — individual service (backend) state.
- `show servicegroup [name]` — service group member states, useful when backends are pooled.
- `stat lb vserver [name]` — real-time hit/throughput counters.

## Monitors (health checks)

- `show lb monitor` — configured monitor types and bindings.
- `show service [name] -summary` — includes monitor probe result and last state-change reason; the first place to look when a service shows DOWN but the backend appears healthy externally.
- Monitor probe failures are frequently the actual root cause of "load balancer is down" reports — always confirm probe type (ping/tcp/http/custom script) matches what the backend actually expects, and check probe source (SNIP) has a valid path to the backend.

## Persistence and SSL

- `show lb vserver [name]` (includes persistence type and timeout in output) — confirm persistence isn't causing uneven distribution or stuck sessions.
- `show ssl vserver [name]` — bound certificate, cipher/protocol config, SSL state.
- `show ssl certkey` — certificate inventory and expiry — expired certs are a very common silent failure cause; check dates directly.

## GSLB (if in use)

- `show gslb vserver [name]` — global server load balancing state across sites.
- `show gslb service` — per-site service health as seen by GSLB.

## Content switching (if in use)

- `show cs vserver [name]` — content switching vserver state and bound policies.
- `show cs policy [name]` — policy expression and binding, confirms correct backend selection logic.

## NAT

- `show inat` — inbound NAT mappings.
- `show rnat` — reverse NAT (outbound) mappings.

## Connections and troubleshooting

- `show connectiontable` — active connection table; filter by IP where supported for targeted lookup.
- `stat system` — overall system throughput/connections-per-second, useful for capacity-related symptoms.
- `nstrace.sh` (shell-level capture, bounded by time/size flags) — packet capture at the ADC; always specify `-time` or `-size` bound and state the bound before running per platform-playbooks.md guardrails.

## Correlation notes

- Frontend/backend separation is the core NetScaler troubleshooting discipline: confirm the client-to-VIP path is healthy (`show lb vserver`, SSL/cert state) separately from the VIP-to-backend path (`show service`, monitor state) before concluding where the fault actually is.
- A vserver in "OUT OF SERVICE" state is administratively disabled — distinguish this explicitly from "DOWN" (monitor-failed) in any report, since the remediation is completely different (re-enable vs fix backend/monitor).
- Persistence misconfiguration (e.g., source-IP persistence behind a NAT/proxy layer masking true client IPs) is a common "uneven load" false lead — check persistence type against the actual client topology before assuming a backend capacity issue.
