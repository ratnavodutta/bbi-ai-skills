# Client Network Agent — automated host evidence collection

A bundled, dependency-free Python runtime (stdlib only) that automates most of the host-level checks in [host-network-troubleshooting.md](host-network-troubleshooting.md) into a single read-only pass, producing timestamped evidence files for the incident record.

## When to use

- Use as the fast path for Phase 2 host-level diagnostics on Windows, Linux, or macOS end-hosts — run it before working through individual commands by hand.
- Still consult [host-network-troubleshooting.md](host-network-troubleshooting.md) for: no-root/no-Administrator privilege tiers, checks the agent doesn't cover (MTU/fragmentation tests, iperf3, packet capture, firewall rule listing), and anything the agent reports as skipped on the target host.
- Do not use it as a substitute for vendor device-side diagnostics — it only runs from the client/end-host, not on network devices.

## Run it

```bash
python scripts/run_client_network_agent.py --target <URL, hostname, IP, or host:port> --output-dir <incident_evidence_dir>
```

Options:

- `--deep` — adds slower optional checks (e.g., Windows `pathping`).
- `--timeout <seconds>` — per-command timeout, default 20.
- `--no-http-body` — for URL targets, collect only HTTP headers and timing, skip the body sample.

## What it collects

- System snapshot: hostname, OS/platform, CPU count, disk usage.
- OS-specific command plan:
  - **Windows**: `ipconfig /all`, `route print`, `netsh interface ipv4 show interfaces`, `ipconfig /displaydns`, `arp -a`, `netstat -ano`, `ping`, `tracert -d`, `nslookup`, optional `pathping` with `--deep`.
  - **Linux**: `ip addr`, `ip route`, resolver state (`resolvectl status` or `/etc/resolv.conf`), NetworkManager hints, `ip neigh`, `ss -s`, `ping`, `tracepath`/`traceroute`, DNS lookup (`getent hosts` / `nslookup`), `iostat` when present.
  - **macOS**: `ifconfig`, `netstat -rn`, `scutil --dns`, `networksetup -listallhardwareports`, `arp -a`, `netstat -an`, `ping`, `traceroute -n`, `nslookup`, `iostat`.
- Python-native checks: DNS resolution (`getaddrinfo`), TCP reachability to host:port, and for URL targets HTTP status/headers/timing plus a curl timing breakdown (DNS/connect/TLS/TTFB/total).

## Output

Two files per run, written to `--output-dir`:

- `client-network-agent-<timestamp>-<target>.json` — full structured evidence.
- `client-network-agent-<timestamp>-<target>.txt` — human-readable rendering of the same evidence.

Attach both to the incident. The JSON's top-level `summary` block (`dns_ok`, `tcp_ok`, `http_ok`, `failed_commands`, `skipped_commands`) is what belongs in Phase 1 hypothesis tracking and the Phase 3 technical summary — do not re-transcribe raw command output into the live response; point to the evidence files instead.

## Boundaries — evidence only

- Collects, does not repair: never changes DNS, routes, firewall, proxy, NIC, DHCP, or MTU settings.
- Does not collect secrets, browser cookies, SSH keys, VPN profiles, or packet captures.
- Does not run destructive load, stress, or write-heavy IOPS tests.
- Uses only OS built-in commands and the Python standard library — nothing to install.
- Bandwidth/throughput load testing is out of scope for this tool; use the manual iperf3/curl-throughput guidance in host-network-troubleshooting.md, and only run it with the user's explicit approval of destination and data volume, consistent with Phase 2's authorization rule.

## If a command comes back skipped

The plan adapts per OS, but a specific binary can still be missing (e.g., no `nslookup` in a minimal container, no `iostat` without sysstat installed). The agent marks that entry `skipped` with a reason instead of failing the run. Treat a skip the same as Phase 2's "identify missing tooling" step — either note it as a gap requiring the tool, or rely on the equivalent Python-native check (`python_checks.dns` / `python_checks.tcp` / `python_checks.http`) already captured in the same evidence file.
