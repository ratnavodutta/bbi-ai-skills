# AWS — Network level

Deep networking design and diagnostic reference. Pairs with platform-playbooks.md's AWS CLI guardrails for live diagnostics; use this file for design depth and less-common failure modes.

## VPC fundamentals an architect must get right up front

- CIDR planning: reserve room for growth, avoid overlap across VPCs/on-prem before any peering or TGW attachment is built — this is the #1 cause of unwindable design mistakes.
- Subnet tiers: public (IGW route), private-with-NAT (egress only), private-isolated (no internet route) — map workload tiers to these explicitly.
- Route tables: one per subnet tier at minimum; never rely on the main route table for anything beyond default-deny-style baseline.
- NACLs (stateless, subnet-level, ordered rules) vs Security Groups (stateful, ENI-level, allow-only) — use SGs as primary control, NACLs for coarse subnet-wide deny/defense-in-depth.

## Connectivity architectures

- **VPC Peering**: non-transitive, simplest for few VPCs, doesn't scale past ~10-15 without becoming unmanageable mesh.
- **Transit Gateway**: hub-and-spoke, transitive routing, supports VPC + VPN + Direct Connect attachments, route tables per attachment for segmentation, appliance mode for stateful inline inspection (symmetric routing requirement).
- **PrivateLink / VPC Endpoints**: Gateway endpoints (S3, DynamoDB — route table based, no ENI) vs Interface endpoints (PrivateLink, ENI + DNS, works for most AWS services and third-party/cross-account services) — prefer PrivateLink over NAT+IGW for AWS service access when security posture demands no internet path.
- **Direct Connect**: dedicated (1/10/100G ports) vs hosted connections; use DX Gateway to fan out one DX to multiple VPCs/regions; pair with Site-to-Site VPN as encrypted backup or for BGP failover; understand DX resiliency models (single connection = no SLA, up to max-resiliency dual-DX-dual-location for mission-critical).
- **Site-to-Site VPN**: IKEv1/v2, BGP or static routing, VPN CloudHub for spoke-to-spoke over VPN, ECMP for aggregate throughput beyond single-tunnel ~1.25 Gbps limit.

## DNS architecture

- Route 53 Resolver: inbound/outbound endpoints for hybrid DNS resolution between on-prem and VPC.
- Private Hosted Zones: associate across VPCs/accounts for shared internal namespace; watch for split-horizon requirements (same domain, different answer inside vs outside).
- Route 53 routing policies: simple, weighted, latency, geolocation/geoproximity, failover, multi-value — map to actual HA/traffic-steering requirement, don't default to simple.

## Load balancing

- ALB (L7, host/path routing, WAF integration) vs NLB (L4, static IP/Elastic IP support, extreme throughput, preserve source IP) vs GWLB (inline traffic inspection via appliances, GENEVE encapsulation).
- Cross-zone load balancing: understand cost and traffic distribution implications when enabled vs disabled.
- Target group health checks: distinguish from instance status checks; a target can be "healthy" at EC2 level and still fail target group health checks due to app-layer issues.

## Security architecture

- AWS Network Firewall: stateful rule groups, domain filtering, IDS/IPS-style suricata rules; deploy centrally via TGW inspection VPC pattern for all-egress inspection.
- Security Group referencing (SG-to-SG rules) over CIDR rules where possible — survives IP churn, self-documenting.
- Flow Logs: VPC-level, subnet-level, or ENI-level; send to CloudWatch Logs for quick query or S3 for cost-effective long retention + Athena querying.

## Common failure domains and what actually causes them

- Asymmetric routing after introducing TGW appliance-mode or NAT gateway placement changes — always verify return path, not just forward path.
- NACL ephemeral port ranges misconfigured after a manual edit — stateless rules need explicit return-traffic allow.
- PrivateLink DNS not resolving to the interface endpoint because private DNS wasn't enabled on the endpoint or the VPC's `enableDnsSupport`/`enableDnsHostnames` are off.
- Cross-account TGW route propagation not enabled on the route table — attachment exists but routes silently don't propagate.
- MTU mismatches across VPN/DX paths (1500 vs jumbo 9001) causing silent fragmentation-drop issues that look like intermittent timeouts.

## Diagnostic tooling beyond basic CLI

- **VPC Reachability Analyzer**: static path analysis between two ENIs/resources without generating traffic — first tool for "is this even possible" questions.
- **VPC Flow Logs + Athena**: historical five-tuple analysis for patterns basic CLI snapshots miss.
- **Traffic Mirroring**: packet-level capture from ENIs to an analysis target when app-layer diagnostics are insufficient.
