# Palo Alto Networks — command reference

CLI (PAN-OS) shown; equivalent views exist in the GUI under Monitor/ACC. Read-only operational commands first. `commit`, `clear session`, `request restart`, HA failover commands, and any `set`/`delete` config-mode entries require explicit authorization.

## System and HA state

- `show system info` — version, model, serial, uptime.
- `show system resources` — CPU/memory/dataplane load; check before deep diagnosis to rule out resource exhaustion.
- `show high-availability state` — HA role (active/passive), sync status, last failover reason.
- `show high-availability all` — full HA config and link/path monitoring state.

## Interfaces and zones

- `show interface all` — admin/link state per interface.
- `show interface [name]` — detailed counters, errors.
- `show zone-protection zone [zone-name]` — zone protection profile state and drop counters.

## Routing

- `show routing route` — RIB.
- `show routing route destination [ip]` — specific route lookup.
- `show routing protocol bgp summary` — BGP peer state.
- `show routing protocol ospf neighbor` — OSPF adjacency state.

## Virtual routers

- `show interface all | match [vr-name]` — confirm interface-to-VR assignment.
- Multiple VRs are a common source of "route exists but traffic still fails" — always confirm the ingress interface's assigned virtual router before trusting a route lookup on the wrong VR.

## Security policy and session

- `show session all` — active session table.
- `show session all filter source [ip] destination [ip]` — targeted session lookup; add `protocol`, `destination-port` as needed to narrow further.
- `show session id [id]` — full detail for one session including NAT translation and applied rule.
- `test security-policy-match from [zone] to [zone] source [ip] destination [ip] protocol [n] destination-port [n]` — simulates policy evaluation without generating traffic; the PAN-OS equivalent of ASA's packet-tracer and the first command for "why is this being blocked/allowed."
- `show counter global filter severity drop` — global drop counters by reason (fastest path to "what's actually dropping and why").

## NAT

- `test nat-policy-match from [zone] to [zone] source [ip] destination [ip] protocol [n] destination-port [n]` — simulates NAT rule evaluation before a session exists.
- `show session all filter nat source [ip]` — confirm actual NAT translation applied to live sessions.

## App-ID and Content-ID

- `show ctd-agent state` / threat log via `show log threat` — content inspection engine state and recent detections.
- App-ID misclassification is a common false "blocked" report — check `show session id [id]` for the identified application vs the expected one; a policy written for one App-ID won't match traffic classified as another.

## VPN (IPsec/GlobalProtect)

- `show vpn ike-sa` — Phase 1 tunnel state.
- `show vpn ipsec-sa` — Phase 2 SA state and traffic counters.
- `show vpn flow` — tunnel interface traffic counters, confirms bidirectional flow.
- `show global-protect-gateway current-user` — connected GlobalProtect sessions.

## Logging (CLI-accessible)

- `show log traffic` — traffic log query from CLI (filterable); GUI Monitor > Traffic is generally faster for iterative filtering.
- `show log system` — system event log, useful for commit history and HA/link events.

## Packet capture

- `debug dataplane packet-diag set filter` (then `on`, then `show`, then `off`) — staged, filtered packet capture; always define the filter and a stop condition before enabling, and disable immediately after capture per platform-playbooks.md guardrails.

## Correlation notes

- Always run `test security-policy-match` before assuming a policy is misconfigured — it shows the actual matching rule including any implicit deny or intrazone-default behavior.
- Confirm virtual router assignment whenever a route "should" exist but traffic fails — multi-VR environments are the most common false "routing" root cause on Palo Alto.
- Cross-check `show counter global filter severity drop` against the session table — a session that never forms won't show in `show session all`, so global drop counters are necessary to catch pre-session drops (e.g., zone protection, packet-based attack protection).
