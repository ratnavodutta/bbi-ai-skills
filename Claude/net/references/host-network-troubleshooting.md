# Host-level network troubleshooting — Windows and Linux

Covers end-host network diagnostics for both operating systems, with an explicit privilege tier for each command so this works on locked-down/high-security systems where root or Administrator is unavailable. Default to the lowest-privilege command that answers the question.

## Privilege tiers — read before selecting commands

- **No elevation required**: works as a standard user on a locked-down machine — safe first choice always.
- **May require elevation**: some environments restrict this to admin/root even though it's conceptually read-only (varies by OS hardening policy) — try unprivileged first, note if it's blocked.
- **Requires elevation**: genuinely needs admin/root by design — flag this as an access gap per Phase 1/2 discipline rather than assuming it's available.

## Windows — connectivity and path

| Task | Command | Privilege |
|---|---|---|
| Reachability | `ping [target]` | No elevation |
| Path trace | `tracert [target]` | No elevation |
| DNS resolution | `nslookup [name]` / `Resolve-DnsName [name]` (PowerShell) | No elevation |
| TCP port reachability (no telnet needed) | `Test-NetConnection [target] -Port [n]` (PowerShell) | No elevation |
| Current IP config | `ipconfig /all` | No elevation |
| Route table | `route print` / `Get-NetRoute` (PowerShell) | No elevation |
| ARP table | `arp -a` | No elevation |
| Active connections | `netstat -ano` | No elevation (process-name mapping via `-b` requires elevation) |
| DNS cache | `ipconfig /displaydns` | No elevation |
| Flush DNS cache | `ipconfig /flushdns` | May require elevation |
| Release/renew DHCP lease | `ipconfig /release` then `/renew` | May require elevation |
| NIC-level statistics | `Get-NetAdapterStatistics` (PowerShell) | No elevation |
| Firewall rule listing | `netsh advfirewall firewall show rule name=all` | May require elevation depending on policy |
| Packet capture | `netsh trace start capture=yes` / Wireshark install | Requires elevation |

## Linux — connectivity and path

| Task | Command | Privilege |
|---|---|---|
| Reachability | `ping [target]` | No elevation (some hardened systems restrict raw ICMP — see fallback below) |
| Path trace | `traceroute [target]` or `tracepath [target]` (tracepath needs no special privilege at all) | No elevation |
| DNS resolution | `dig [name]` / `nslookup [name]` / `getent hosts [name]` | No elevation |
| TCP port reachability without root | `bash -c 'cat < /dev/tcp/[target]/[port]'` (bash built-in, no nc/telnet needed) or `curl -v telnet://[target]:[port]` | No elevation |
| Current IP config | `ip addr show` (`ifconfig` deprecated but often still present) | No elevation |
| Route table | `ip route show` | No elevation |
| ARP/neighbor table | `ip neigh show` | No elevation |
| Active connections | `ss -tunap` | No elevation for socket list; process-owner detail may be limited to own processes without root |
| Interface statistics | `ip -s link show [iface]` | No elevation |
| DNS config in use | `cat /etc/resolv.conf` | No elevation |
| Packet capture | `tcpdump` | Requires elevation (or `CAP_NET_RAW` capability granted) |
| Firewall rule listing | `iptables -L -n` / `nft list ruleset` | Requires elevation |

## Working around no-root / no-admin access

This is the common real-world constraint on secured hosts — the goal is proving or disproving reachability and path health using only tools that don't need elevated rights.

- **TCP port test without nc/telnet/root**: `/dev/tcp` bash redirection (Linux) or `Test-NetConnection -Port` (Windows PowerShell) both work unprivileged and confirm L4 reachability precisely — use these before asking for elevated access.
- **HTTP/HTTPS-layer test**: `curl -v [url]` or `curl -o /dev/null -s -w '%{time_connect} %{time_starttransfer} %{time_total}\n' [url]` — gives connect time, TLS handshake time, and total time breakdown without any special privilege, useful for isolating "is it network or is it the app" without a packet capture.
- **DNS-layer isolation**: compare `dig @[specific_dns_server] [name]` against the default resolver — isolates DNS server-specific failures from general resolution failures, no privilege needed.
- **MTU/fragmentation test without admin capture tools**: `ping -M do -s [size] [target]` (Linux, adjust size to test path MTU) or `ping -f -l [size] [target]` (Windows) — both work unprivileged (standard ICMP ping privilege) and can isolate path MTU issues without a packet capture.
- **Application-layer loop-back proof point**: if a browser/app can reach the target but CLI tools can't, capture the exact error text and timing from the app itself (dev tools network tab, app logs) rather than assuming CLI parity — proxy/SSO/client-specific behavior can differ from raw socket tests.
- **When truly nothing below app-layer is available**: document precisely what was and wasn't testable, and hand the remaining L2/L3 verification to whoever holds elevated access as a discrete authorized action rather than blocking the whole triage on it — this keeps Phase 1's roadmap moving.

## Bandwidth / throughput / consumption checks during troubleshooting

Use to distinguish a capacity/congestion problem from a connectivity/routing/policy problem — run only after basic reachability is confirmed, since a saturated link can look identical to a broken one at the ping/traceroute layer.

### No-elevation-required options

- **iperf3 in client mode** (if a matching server exists at the other end, common in enterprise environments for exactly this purpose): `iperf3 -c [server] -t 10` — no root needed for client mode; reports actual achievable throughput, not just link speed.
- **curl-based rough throughput estimate** against a large known file/endpoint: `curl -o /dev/null -w '%{speed_download}\n' [url]` — approximate, but useful when iperf3 isn't available and no elevation exists.
- **Windows `Get-NetAdapterStatistics` / Linux `ip -s link`** — cumulative interface byte/packet counters; take two snapshots a known interval apart to calculate an approximate rate without any monitoring tool installed.
- **Windows Task Manager > Performance > [adapter]** or **Resource Monitor > Network tab** — live per-process and per-adapter throughput, GUI-accessible without admin on most builds.
- **Linux `/proc/net/dev`** — raw counters readable by any user (`cat /proc/net/dev`), same two-snapshot-delta technique as `ip -s link` when even that's restricted.

### Requires elevation or infrastructure access

- `tcpdump` + post-capture analysis (Wireshark I/O graph) for granular per-flow bandwidth breakdown.
- SNMP polling of interface counters (`ifHCInOctets`/`ifHCOutOctets`) from network device side — often the most reliable source of truth since it's independent of host-side restrictions entirely; prefer this path when the host is locked down but you have device management access.
- NetFlow/sFlow/IPFIX export analysis for top-talker and application-level bandwidth breakdown across the network, not just one host.

## Correlation notes

- Always separate "can't connect" from "connects but slow" explicitly in the incident record — they point to different hypothesis branches (routing/ACL/policy vs capacity/congestion/duplex mismatch).
- A duplex mismatch or a saturated link both produce intermittent, load-correlated symptoms that look identical to application-layer flakiness — check interface error/utilization counters (host-side via the tables above, or device-side via the vendor command references) before spending time on app-layer hypotheses when symptoms correlate with load or time-of-day.
- On locked-down hosts, prefer building the evidence chain entirely from no-elevation tools first and only request elevated access for the specific remaining gap — this keeps Phase 2's "confirm access before commands" step honest and minimizes friction with security teams.
