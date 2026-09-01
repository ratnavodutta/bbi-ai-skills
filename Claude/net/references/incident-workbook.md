# Canonical incident workbook

Maintain one workbook per incident unless explicitly asked for more files. Update an existing workbook in place and reuse matching sheets.

## Recommended sheets

1. `Incident Summary`: identity, severity, owner/status, timestamps, impact, scope, finding, confidence, restoration, risk, milestone.
2. `Scope & Topology`: endpoints, protocol/port, path, environments, zones/VRFs/VNets/VPCs, NAT, comparisons, changes, unknowns.
3. `Timeline`: timestamp, source, event/action, observation, impact, decision.
4. `Hypotheses`: ID, evidence, likelihood/impact, test, expected/actual result, disposition, next step.
5. `Diagnostics`: timestamp, platform/target/context, command/query, purpose, summarized output, interpretation, source, operator.
6. `Actions`: type, owner, authorization/change ID, risk, rollback, status, timestamp, result.
7. `Validation & Follow-up`: criterion, method/result/evidence, monitoring window, owner, due date, status.

Omit irrelevant sheets. Use tables, filters, frozen headers, wrapped text, readable widths, consistent timestamps, and restrained status colors. Summarize raw command output and reference its source.

## Update rules

- Locate records by stable incident and hypothesis/action IDs, not row number.
- Append chronology/diagnostics; update current-state fields in place.
- Preserve formulas, validation, tables, named ranges, formatting, hidden sheets, and unrelated content.
- Do not create timestamped, `final`, exported, or companion copies unless asked.
- Record confidence as `Confirmed`, `Probable`, `Possible`, or `Unresolved`.
- Mask sensitive data and verify formulas, filters, layout, names, and that only the intended workbook changed.
