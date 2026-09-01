# Troubleshooting method

## Evidence model

Classify each item as `Reported`, `Observed`, `Inferred`, `Unknown`, or `Confirmed`. Attach source and timestamp to every material observation. Confirm root cause only when evidence explains the symptom and remediation restores success criteria.

## Scoping record

Capture incident metadata and impact; source, destination, protocol/port, direction, NAT and DNS; routing/security/load-balancer domains; frequency and working-versus-failing cases; last known good and changes; errors, logs, flows, packets and health; owners, access gaps, and change constraints. Mark unavailable fields unknown and continue safe triage.

## Hypotheses

Record failure domain, evidence for/against, likelihood/impact, discriminating test, expected signal, actual result, disposition, and next branch. Prefer tests that are safe, fast, and divide the hypothesis space sharply.

## Layered path

Evaluate endpoint, DNS, L2/L3, overlay/underlay, security/NAT, VPN/transit, load balancer, application listener, and return-path symmetry. Let evidence override this order.

## Closure

Require recovery against the original flow, supporting telemetry, an appropriate stability interval, documented change/rollback state, dated follow-up owners, and residual risk. If causality is unproven, label the incident restored but root cause unconfirmed.
