# AWS — Architect level

Use for design reviews, HLD/LLD, migration planning, cost/resilience trade-offs, and Well-Architected assessments. Not for live incident diagnostics — see aws-network.md and platform-playbooks.md for that.

## Well-Architected pillars — apply as a checklist

- **Operational excellence**: IaC (CloudFormation/CDK/Terraform), runbooks, game days, observability (CloudWatch, X-Ray), change management via pipelines not console.
- **Security**: least privilege IAM, SCPs at Organizations level, KMS CMKs vs AWS-managed keys, GuardDuty/Security Hub/Config, network segmentation by account (landing zone) before subnet-level controls, encryption in transit and at rest by default.
- **Reliability**: define RTO/RPO first, then pick Multi-AZ vs Multi-Region, health checks and self-healing (ASG, ELB), Route 53 failover/latency routing, backup/restore tested not assumed.
- **Performance efficiency**: right compute family for workload (compute/memory/storage optimized), caching tiers (CloudFront, ElastiCache, DAX), read replicas vs Aurora Global Database, placement groups for low-latency clusters.
- **Cost optimization**: Savings Plans/RIs for steady-state, Spot for fault-tolerant/batch, S3 storage classes and lifecycle policies, right-sizing via Compute Optimizer, tagging strategy for cost allocation.
- **Sustainability**: consolidate underutilized resources, prefer managed/serverless where workload pattern fits, region selection where carbon data matters to the org.

## Landing zone / multi-account structure

- AWS Organizations with OUs: Security, Infrastructure, Workloads (per environment), Sandbox.
- Control Tower for guardrails (preventive via SCP, detective via Config rules).
- Centralized logging account (CloudTrail org trail, centralized S3 + Athena/QuickSight).
- Network account owning Transit Gateway, shared via RAM to spoke accounts.
- Separate accounts per environment (dev/stage/prod) minimum; per major workload for blast-radius isolation at scale.

## Compute architecture decisions

- EC2 vs ECS vs EKS vs Lambda: decide on statefulness, execution duration, scaling granularity, team's container maturity.
- ASG scaling policies: target tracking for steady load, step scaling for spiky, predictive scaling for known cyclic patterns.
- EKS: managed node groups vs Fargate profiles vs Karpenter for node provisioning; IRSA for pod-level IAM instead of node-wide roles.

## Data and storage architecture

- RDS Multi-AZ (sync standby, HA) vs read replicas (async, scale-out reads) vs Aurora (storage-layer replication, faster failover, Global Database for cross-region).
- DynamoDB: on-demand vs provisioned capacity, GSI design to avoid hot partitions, DAX for read-heavy microsecond latency, Global Tables for multi-region active-active.
- S3: versioning + lifecycle + Object Lock for compliance/immutability, Cross-Region Replication for DR, S3 Access Points for shared-bucket multi-tenant access.

## Resilience patterns

- Design for failure at every AZ boundary; never single-AZ for anything production-critical.
- Circuit breakers and retries with exponential backoff + jitter for service-to-service calls.
- Bulkhead pattern via separate ASGs/queues per tenant or criticality tier to contain blast radius.
- Chaos/game-day testing (AWS Fault Injection Simulator) to validate assumed resilience, not just design it.

## Migration and modernization framework

- 6 R's: Rehost, Replatform, Repurchase, Refactor, Retire, Retain — map each app portfolio item explicitly, don't default to lift-and-shift.
- Application Discovery Service / Migration Hub for dependency mapping before wave planning.
- Database migration: DMS for heterogeneous/homogeneous with minimal downtime via CDC.

## Cost and governance instruments an architect should reference

- Cost Explorer + Budgets + anomaly detection for ongoing governance.
- AWS Config conformance packs to enforce architecture standards at scale, not just document them.
- Well-Architected Tool for structured, repeatable review documentation per workload.

## When asked for HLD/LLD

Produce: context diagram (trust boundaries, external integrations), component diagram (services + data stores), network diagram (VPCs, connectivity, security boundaries — see aws-network.md), non-functional requirements mapped to design decisions (why this instance family, why this failover model), and an explicit list of trade-offs made and alternatives rejected with reasons.
