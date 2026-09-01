# Azure — Architect level

Use for design reviews, HLD/LLD, landing zone planning, and Well-Architected Framework assessments. Not for live incident diagnostics — see azure-network.md and platform-playbooks.md for that.

## Well-Architected Framework pillars — apply as a checklist

- **Reliability**: define availability SLA target first, then pick Availability Zones vs Region Pairs vs both; Azure SLA is composite across the chain (compute + storage + network) — architect to the weakest link.
- **Security**: Zero Trust as default posture, Azure Policy for guardrails, Defender for Cloud for posture management, Key Vault for secrets/keys/certs, Private Endpoints over service endpoints where compliance demands no public path.
- **Cost optimization**: Azure Hybrid Benefit for licensed workloads, Reserved Instances/Savings Plans for steady-state, right-sizing via Azure Advisor, Cost Management + Budgets with alerts.
- **Operational excellence**: IaC via Bicep/Terraform (not portal-first for production), Azure Monitor + Log Analytics as the single observability plane, deployment via Azure DevOps/GitHub Actions pipelines.
- **Performance efficiency**: choose VM series to workload profile (Dv5 general, Ev5 memory, Fsv2 compute, Lsv3 storage-IO), autoscale rules tied to actual bottleneck metric not just CPU, Azure Front Door/CDN for global performance.

## Landing zone (Cloud Adoption Framework) structure

- Management group hierarchy: Root → Platform (Identity, Management, Connectivity) → Landing Zones (per environment/workload) → Sandbox/Decommissioned.
- Connectivity subscription owns the hub VNet, ExpressRoute/VPN gateways, Azure Firewall — spokes peer in, never own their own internet egress independently in a hub-spoke model.
- Azure Policy assigned at management group level for guardrails that apply org-wide (allowed regions, mandatory tags, encryption enforcement); assigned narrower at subscription level for workload-specific rules.
- Subscription democratization: one subscription per major workload/environment for blast-radius and quota isolation, not one subscription for everything.

## Compute architecture decisions

- VM Scale Sets (uniform vs flexible orchestration) vs AKS vs App Service vs Azure Functions — decide on statefulness, container maturity, cold-start tolerance.
- AKS: node pools segmented by workload (system vs user pools), Azure CNI vs kubenet (CNI required for advanced network policy/Windows nodes), Workload Identity for pod-level auth instead of node MSI.
- Availability Sets (rack-level fault domain, single datacenter) vs Availability Zones (datacenter-level, requires zone-aware SKUs) — never mix reliability assumptions between them.

## Data and storage architecture

- SQL: Business Critical tier (built-in AG, low-latency HA) vs General Purpose (remote storage, cheaper, higher failover latency); Auto-failover groups for cross-region DR with automatic endpoint redirection.
- Cosmos DB: consistency level selection (Strong through Eventual) is a real architectural trade-off, not a default checkbox; multi-region writes need conflict resolution policy defined upfront.
- Storage: redundancy tiers LRS/ZRS/GRS/GZRS mapped to actual RPO requirement; Private Endpoints for storage accounts holding sensitive data.

## Resilience patterns

- Design across Availability Zones as default for anything production in a zone-enabled region; Region Pairs for the region-level disaster scenario, not routine HA.
- Traffic Manager (DNS-level, any protocol) vs Front Door (HTTP/S, L7, WAF+caching+global routing) vs Load Balancer (regional L4) — pick by layer and scope needed, commonly layered together.
- Retry with exponential backoff for transient faults against PaaS services (documented as expected behavior for SQL DB, Storage, Service Bus).

## Migration and modernization framework

- Azure Migrate for discovery/assessment/dependency mapping before wave planning.
- 5 R's commonly used in CAF: Rehost, Refactor, Rearchitect, Rebuild, Replace — map portfolio explicitly.
- Database Migration Service for minimal-downtime migration with CDC where source supports it.

## Governance instruments an architect should reference

- Azure Policy (deny/audit/deployIfNotExists effects) plus initiative definitions for bundled compliance standards.
- Management group-level Cost Management views plus subscription budgets with action-group-triggered alerts.
- Azure Advisor and Well-Architected Review (via Azure landing zone review tooling) for structured, repeatable assessment.

## When asked for HLD/LLD

Produce: context diagram (trust boundaries, external integrations), component diagram (services + data stores), network diagram (hub-spoke topology, connectivity, security boundaries — see azure-network.md), non-functional requirements mapped to design decisions, and an explicit trade-off list with rejected alternatives and reasons.
