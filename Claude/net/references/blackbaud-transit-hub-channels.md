# Blackbaud transit-hub Slack channels

Read this when a Blackbaud network/cloud question mentions Slack, alerts, PRs, or change requests for
the AWS/Azure "transit hub," or when deciding which channel to check first. It exists so /net does not
have to rediscover this channel map from scratch on every incident.

## How this list was built — read before trusting it blindly

Slack sidebar "sections" (e.g. a personal category someone calls "Cloud") are a per-user UI preference,
not a shared object — there is no API access to another user's sidebar, and two users can group the same
channels under different section names or no section at all. **Always resolve by channel name, never by
a sidebar section.** The channels below were found by keyword search (`azure`, `aws`, `transit-hub`,
`network`, `cloud`, `zscaler`) plus direct reads, not by reading anyone's sidebar. Confirm with the user
if a channel relevant to their question is missing from this list.

## Channel map

| Channel | ID | Kind | Cloud / env | What it actually is |
|---|---|---|---|---|
| `#azure-transit-hub-alerts-nonprod` | `C09NT21J6LB` | Automated Azure Monitor alerts | Azure, E01 (test) | Function App "unauthorized client" Sev1 noise (the dominant volume) plus a confirmed Sev0 LB/DIP network-alert cluster. Fully mined — see the canonical incident workbook for the alert log, episodes, and root-cause evidence. |
| `#azure-transit-hub-alerts-prod` | `C07JEHG47PA` | Automated Azure Monitor alerts | Azure, N01 (production) | Same Function App noise family plus 8 more genuine network/platform alert types (LB/FW health, DIP fleet vs. instance, VIP, VM/VMSS CPU, spoke-VM utilization). Fully mined — see the canonical incident workbook. |
| `#aws-transit-hub-alerts-prod` | `C09FAAG51B9` | Automated alerts (Amazon Q) | AWS, production | AWS equivalent of the Azure prod alerts channel. Not yet mined in depth — treat any AWS-side alert findings here as unverified until sampled the same way the Azure channels were. |
| `#aws-transit-hub-alerts-nonprod` | `C09NRQSPJ11` | Automated alerts (Amazon Q) | AWS, non-production | AWS equivalent of the Azure nonprod alerts channel. Not yet mined in depth. |
| `#azure-transit-hub-pr` | `C0A04PXJXL1` | Automated PR feed (Azure Repos bot) | Azure | Pull-request activity for the Azure transit-hub Terraform/IaC repo. Useful for "what changed recently" — not an alert channel, don't expect incident content here. |
| `#aws-transit-hub-pr` | `C09V9E7P7GC` | Automated PR feed (Azure Repos bot) | AWS | Same idea for the AWS transit-hub IaC repo. Note the bot is still "Azure Repos" — the AWS infra's source of truth is hosted in Azure DevOps too. |
| `#transit-hubs-aws` | `C0916V8RNS2` | Human coordination | AWS, cross-env | Where engineers ask for egress-IP allow-listing, firewall-rule changes, CIDR overlap checks, and coordinate cutovers. Good source for "why did someone change X" context; not a monitoring feed. |
| `#transit-hub-private` | `C0ABMTC9799` | Human coordination — **private/restricted** | Cross-cloud | Working-team channel (leads + a few engineers) for migration status, OpsGenie enablement decisions, and higher-level planning. Access-gated — don't assume /net or any given user can read it, and don't quote its content into shared artifacts; describe its existence and purpose only. |
| `#cm-transit-hubs` | `C0ACT4QT1U7` | Change-management interface | Cross-cloud | Where engineers ask Blackbaud's Change Management team to schedule, reschedule, or close ServiceNow RFCs for transit-hub changes. Ticketing/process only, not technical alert content. |
| `#jg-network-moderization-transit-hub` | `C092X82BBN0` | Human coordination, scoped to one business unit | Cross-cloud | "jg" = JustGiving (an acquired Blackbaud platform). Tracks that BU's specific network-modernization and transit-hub cutover work (prod-data, prod-backoffice, CDE). Don't generalize findings from here to the rest of Blackbaud's transit hub. |

## Practical guidance for /net

- For an active alert/incident question about Azure transit hub: start with whichever of the two
  `azure-transit-hub-alerts-*` channels matches the environment named in the report, then check
  `#azure-transit-hub-pr` for a recent change that might explain onset.
- For AWS transit hub: same pattern with the `aws-transit-hub-alerts-*` and `#aws-transit-hub-pr`
  channels, but treat AWS-side alert-type classification as unverified until it's been sampled the way
  the Azure channels were (see the incident workbook's methodology).
- For "why was this changed" or "is a change in flight": check `#transit-hubs-aws` (AWS) or the relevant
  PR channel, and `#cm-transit-hubs` for the formal RFC/change-request status.
- Do not surface `#transit-hub-private` content in any artifact meant for broad sharing — summarize that
  it exists and what kind of discussion happens there, not what was said.
- This map is Blackbaud-specific. A skill user outside Blackbaud, or a channel renamed/archived since this
  was written, means this table should be treated as a starting point to verify, not a guarantee.
