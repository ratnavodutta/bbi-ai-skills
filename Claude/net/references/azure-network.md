# Azure — Network level

Deep networking design and diagnostic reference. Pairs with platform-playbooks.md's Azure CLI guardrails for live diagnostics; use this file for design depth and less-common failure modes. Aligns with AZ-700 scope.

## VNet fundamentals an architect must get right up front

- Address space planning across hub, spokes, on-prem, and any future M&A/multi-cloud CIDRs before any peering or gateway is built — overlap is the single hardest thing to unwind later.
- Subnet design: dedicated subnets required for AzureFirewallSubnet, GatewaySubnet, AzureBastionSubnet — these have fixed naming and minimum size requirements, get them wrong and redeployment is disruptive.
- NSGs (stateful, subnet or NIC level) as primary control; Application Security Groups to group NICs logically instead of maintaining IP lists in NSG rules.
- Route tables (UDRs): required to force traffic through NVA/Azure Firewall instead of default system routes; watch for the "0.0.0.0/0 to NVA" pattern breaking Azure control-plane traffic unless service tags/BGP routes are excluded properly.

## Connectivity architectures

- **VNet Peering**: non-transitive by default, low-latency backbone path, no transitive routing unless paired with a hub NVA/Firewall or using Virtual WAN.
- **Azure Virtual WAN**: managed hub-and-spoke at scale, transitive routing built in, integrates ExpressRoute/VPN/SD-WAN partner integration, hub route tables for segmentation (this is the modern replacement for manually-built hub-spoke with an NVA when transitive routing at scale is the requirement).
- **ExpressRoute**: private, non-internet circuit via connectivity provider; Standard vs Premium (global reach, higher route limits) vs Local (cost-optimized, co-located); ExpressRoute Gateway SKU (ErGw1AZ/2AZ/3AZ, zone-redundant options) sized to throughput and connection count needs; use Global Reach to connect on-prem sites to each other via the Microsoft backbone.
- **VPN Gateway**: Site-to-Site (IKEv1/v2, active-active for higher throughput/resilience), Point-to-Site (client VPN, certificate or Azure AD auth), VPN as ExpressRoute backup via coexisting gateways in the same VNet.
- **Private Link / Private Endpoints**: NIC injected into your VNet mapped to a PaaS service, eliminates public exposure; Private DNS Zones must be linked correctly or resolution silently falls back to public endpoint.

## DNS architecture

- Azure Private DNS Zones linked to VNets for internal resolution; Private Resolver (replacing older DNS forwarder VM patterns) for hybrid DNS between on-prem and Azure without needing a custom VM-based forwarder.
- Split-horizon considerations when the same FQDN must resolve differently for internal vs external clients (common with Private Link).

## Load balancing

- Azure Load Balancer (L4, regional or global tier, Standard SKU required for zone-redundancy) vs Application Gateway (L7, WAF_v2 SKU integrates WAF, path-based routing, autoscaling) vs Front Door (global L7, anycast, edge caching + WAF) — commonly layered: Front Door → App Gateway → internal Load Balancer.
- Application Gateway health probes distinguish backend pool health from listener-level issues — a common false "gateway is broken" report is actually a backend health probe misconfiguration.

## Security architecture

- Azure Firewall (stateful, FQDN filtering, threat intelligence, forced-tunneling support) as the central egress/inspection point in a Virtual WAN secured hub or hub-spoke pattern.
- NSG Flow Logs (via Network Watcher) plus Traffic Analytics for visualized flow patterns instead of raw log parsing.
- DDoS Protection Standard for internet-facing VNets carrying production traffic — Basic tier is platform-default and insufficient for anything business-critical.

## Common failure domains and what actually causes them

- Effective routes showing a UDR that silently breaks Azure platform traffic (e.g., forcing all 0.0.0.0/0 through an NVA without excluding required service tags) — always check Effective Routes on the NIC, not just the route table definition.
- Private Endpoint DNS not resolving correctly because the Private DNS Zone isn't linked to the *consuming* VNet, only the hub — a very common oversight in hub-spoke designs.
- Asymmetric routing after adding a second NVA/Firewall instance without validating that both forward and return paths transit the same appliance.
- NSG rule priority collisions after manual edits — lower number wins, and a broad deny inserted at a low priority number silently overrides intended allows below it.
- ExpressRoute route limit exceeded (silent prefix drop) after connecting more on-prem summarized routes than the circuit SKU supports.

## Diagnostic tooling beyond basic CLI

- **Network Watcher — Connection Troubleshoot / IP Flow Verify**: validate reachability and NSG rule evaluation without generating real traffic first.
- **Network Watcher — Effective Routes / Effective Security Rules**: see the actual computed state on a NIC, not just what's configured at each layer.
- **Network Watcher — Packet Capture**: targeted, bounded VM-level capture when app-layer diagnostics are insufficient.
- **Azure Monitor Network Insights**: topology-aware health view across ExpressRoute, VPN, Load Balancer, and Firewall in one place for faster triage.
