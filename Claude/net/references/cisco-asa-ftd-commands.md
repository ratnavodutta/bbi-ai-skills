# Cisco ASA & FTD — command reference

Read-only first. `clear`, `packet-tracer` is safe/non-disruptive and encouraged; `capture` is safe if bounded (filter + limited duration/size) — state the bound before running. Config changes, `write memory`, `reload`, and failover actions require explicit authorization.

## ASA — interface and system state

- `show interface ip brief` — interface up/down and IP summary.
- `show interface detail` — errors, drops, duplex/speed per interface.
- `show nameif` — interface-to-security-zone name mapping.
- `show failover` / `show failover state` — HA role, sync state, last failover reason.
- `show version` — code version, licensed features, uptime.
- `show cpu usage` / `show memory` — resource exhaustion check before deeper diagnosis.

## ASA — routing

- `show route` — RIB.
- `show route [prefix]` — specific route detail and source.
- `show asp table routing` — accelerated security path routing lookup, useful when `show route` looks correct but traffic still fails.

## ASA — NAT

- `show nat` — configured NAT rules.
- `show xlate` — active translations.
- `show nat detail` — per-rule hit counts.
- `packet-tracer input [interface] tcp/udp [src_ip] [src_port] [dst_ip] [dst_port]` — simulates a flow through the entire policy chain (NAT, ACL, routing, inspection) without sending real traffic; this is the single most valuable ASA/FTD diagnostic command.

## ASA — access control and policy

- `show access-list [name]` — ACE hit counters.
- `show access-list [name] | include [ip]` — filter large ACLs to relevant entries.
- `show conn` — active connection table; filter by `show conn address [ip]`.
- `show conn detail` — includes flags (NAT state, flow type) per connection.
- `show local-host [ip]` — per-host connection/xlate/inspect state, useful for troubleshooting a single endpoint.

## ASA — VPN

- `show crypto isakmp sa` / `show crypto ikev2 sa` — Phase 1 tunnel state.
- `show crypto ipsec sa` — Phase 2 SA state, encaps/decaps counters (confirms bidirectional traffic flow).
- `show vpn-sessiondb detail anyconnect` — remote-access VPN session detail.
- `show vpn-sessiondb summary` — session counts by tunnel type, useful for license/capacity triage.

## ASA — inspection and drops

- `show asp drop` — accelerated security path drop reasons; the fastest way to see *why* ASA is dropping traffic (fragmentation, no route, ACL deny, conn limit, etc.).
- `show asp drop flow-cache` — clears/summarizes accumulated drop counters.
- `show service-policy` — applied MPF policies and inspection hit counts.

## FTD — Firepower-specific layer (managed via FMC or FDM; CLI available via SSH/console)

- `show managers` — FMC registration status; confirm device is actually in sync before trusting policy state.
- `show running-config` (LINA/ASA layer, via `system support diagnostic-cli` from FTD CLI) — underlying ASA-equivalent config.
- `show snort statistics` — Snort engine health, packets processed/dropped, useful when FTD passes ASA-layer checks but still drops traffic at the inspection engine.
- `system support firewall-engine-debug` — real-time per-flow trace through the Snort/access-control policy engine; requires specifying source/destination filters — bound it.
- `show access-control-config` — deployed ACP summary from CLI.
- FMC UI/API: Analysis > Connection Events for policy-hit-level visibility that CLI alone won't show cleanly.

## Deployment state awareness (FTD)

- Always confirm the last successful policy deployment time before troubleshooting — a config that looks correct in FMC but hasn't deployed is a very common false lead.
- `show version` on FTD includes both the platform (Firepower) and software (FTD) version; version-specific syntax and Snort engine version (Snort 2 vs Snort 3) both affect available commands and behavior.

## Correlation notes

- On both ASA and FTD, `packet-tracer` should be the first diagnostic step for any "traffic isn't passing" report — it identifies the exact policy stage (route lookup, NAT, ACL, inspection) causing the drop before any capture is needed.
- `show asp drop` counters are cumulative since last clear/reload — note the counter baseline before and after reproducing the issue to isolate relevant drops from background noise.
- For FTD, always separate LINA-layer (ASA-equivalent packet forwarding) issues from Snort-layer (inspection/ACP) issues — they have separate counters and separate failure modes.
