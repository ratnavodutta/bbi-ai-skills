# Cisco Meraki — troubleshooting reference

Meraki is cloud-managed: most diagnostics happen via Dashboard UI or Dashboard API rather than device CLI. Local CLI access is limited/vendor-restricted, so this reference centers on Dashboard tools and API calls. Treat firmware pushes, config template changes, and network-wide policy changes as high-impact per platform-playbooks.md guardrails.

## Dashboard — first-look tools

- **Network-wide > Health** (or **Organization > Overview**) — quick device/client status roll-up before drilling into one device.
- **Network-wide > Event log** — chronological device events (DHCP, VPN, client connect/disconnect, config changes); filter by device or client, this is usually the fastest path to a timeline.
- **Organization > Change log** — audit trail of dashboard configuration changes; check this first when a "sudden" issue correlates with a recent change.

## Per-device diagnostics (Dashboard)

- **Device > Tools tab**: contains live diagnostics without needing device CLI —
  - **Ping** — from the device itself to a target.
  - **Throughput test** — MX/switch-to-cloud or device-to-device throughput.
  - **Cable test** (switches) — physical cable diagnostics per port.
  - **ARP table**, **Live tools > Wireless/Air Marshal** (APs) — client and RF-layer visibility.
- **Live Tools API/UI "Ping device"** and **"Throughput test"** are non-disruptive and safe to run without prior authorization; they generate bounded test traffic only.

## MX (security appliance) specific

- **Security & SD-WAN > Route table** — MX-side RIB.
- **Security & SD-WAN > VPN status** — Auto VPN / non-Meraki VPN tunnel state, useful for hub-spoke SD-WAN troubleshooting.
- **Security & SD-WAN > Firewall** — L3/L7 rule hit visibility (via Event log filtering, not a live counter view like traditional firewalls).
- **Uplink Status** (Organization or Network level) — WAN interface state, useful for SD-WAN failover troubleshooting.

## MS (switch) specific

- **Switch > Switch ports** — per-port status, VLAN, PoE draw, errors.
- **Switch > Monitor > Switch port** — packet counters and error counters per port.
- STP and L2 loop detection surfaces via Event log entries (`STP` events) rather than a live `show spanning-tree` equivalent.

## MR (wireless) specific

- **Wireless > Monitor > Access points** — per-AP client count, channel, utilization.
- **Wireless > RF Profiles** — channel/power config affecting interference-related symptoms.
- **Air Marshal** — rogue AP / interference detection.

## API-based diagnostics (when Dashboard UI access is limited or bulk data is needed)

- `GET /organizations/{organizationId}/devices/statuses` — bulk device up/down status.
- `GET /networks/{networkId}/clients` — client inventory with usage stats.
- `POST /devices/{serial}/liveTools/ping` then `GET /devices/{serial}/liveTools/ping/{pingId}` — programmatic ping (async job pattern — submit then poll).
- `POST /devices/{serial}/liveTools/throughputTest` — programmatic throughput test, same async pattern.
- `GET /networks/{networkId}/events` — programmatic event log pull, useful for correlating timestamps across many devices at once.
- All Live Tools API calls are async: submit the job, then poll the result endpoint with the returned ID — do not assume synchronous response.

## Correlation notes

- Because Meraki centralizes config and telemetry in the cloud, always check **Organization > Change log** for a correlating config change before assuming a device-side fault — cloud-pushed misconfiguration is a more common root cause here than on box-managed platforms.
- MX Auto VPN issues often trace back to one hub/spoke reporting a different firmware version — check firmware consistency across the VPN mesh via **Organization > Firmware upgrades** before deep tunnel diagnostics.
- Live Tools (ping/throughput/cable test) run from the device itself, not from the admin's browser — results reflect the device's actual network position, making them more reliable than client-side tests for on-site connectivity questions.
