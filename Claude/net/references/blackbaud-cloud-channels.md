# Blackbaud "Cloud" Slack channel directory

Read this when a Blackbaud network/cloud question mentions Slack, alerts, PRs, change requests, or asks
"which channel do I check" — this maps every channel one Blackbaud user grouped under a personal sidebar
category, verified by reading each channel directly. It exists so /net doesn't have to rediscover this
channel map from scratch on every incident.

## How this list was built — read before trusting it blindly

Slack sidebar "sections" (e.g. a personal category someone calls "Cloud") are a per-user UI preference,
not a shared Slack object — there is no API to enumerate another user's sidebar, and two users can group
the same channels under different names or no section at all. **Always resolve by channel name, never by
a sidebar section.** Every channel below was confirmed by directly reading its message history (not by
keyword guessing) — each row's "what it actually is" reflects real messages seen, not assumption. If a
channel relevant to your question isn't in this table, it wasn't in the section this was built from;
confirm with the user rather than guessing.

Two channels here (`#engineeringsystem`, `#intelligent-platform-group`) turned out **not** to be
network/cloud-infrastructure channels at all once read — they're kept in the table so the map stays
complete and accurate, but they're flagged so /net doesn't misroute a request to them.

## Channel map

### AWS / Azure transit-hub — automated alerts

| Channel | ID | Cloud / env | What it actually is |
|---|---|---|---|
| `#azure-transit-hub-alerts-nonprod` | `C09NT21J6LB` | Azure, E01 (test) | Automated Azure Monitor alerts (posted by Slackbot/webhook), *plus* human triage in the same channel — e.g. Doug Smart and Sampath Mentraddi discussing root cause and linking the fix PR directly in-thread. Dominant pattern: Function App "unauthorized client" IP-allow-list-drift noise. Fully mined — see the canonical incident workbook for the alert log and evidence. |
| `#azure-transit-hub-alerts-prod` | `C07JEHG47PA` | Azure, N01 (production) | Same alert delivery pattern (Slackbot-posted Azure Monitor alerts), production environment. Broader alert-type diversity than nonprod (LB/FW health, DIP fleet vs. instance, VIP, VM/VMSS CPU). Fully mined — see the canonical incident workbook. |
| `#aws-transit-hub-alerts-prod` | `C09FAAG51B9` | AWS, production | Automated alerts posted by the "Amazon Q" bot — AWS's equivalent of the Azure Monitor-to-Slack pattern. High message volume, mostly unlabeled bot posts (content requires opening each message/card, not just the preview). Not yet mined to the same depth as the Azure channels — treat alert-type classification here as unverified. |
| `#aws-transit-hub-alerts-nonprod` | `C09NRQSPJ11` | AWS, non-production | Same Amazon Q bot pattern, nonprod. Not yet mined in depth. |

### AWS / Azure transit-hub — automated PR feeds

| Channel | ID | Scope | What it actually is |
|---|---|---|---|
| `#azure-transit-hub-pr` | `C0A04PXJXL1` | Azure | "Azure Repos" bot posting pull-request activity for the Azure transit-hub Terraform/IaC repo. Pure change feed — useful for "what changed recently," not an incident/alert source. |
| `#aws-transit-hub-pr` | `C09V9E7P7GC` | AWS | Same "Azure Repos" bot, posting PR activity for the AWS transit-hub IaC repo — the AWS infra's source of truth is hosted in Azure DevOps too, hence the bot name mismatch. Pure change feed. |

### AWS / Azure transit-hub — human coordination

| Channel | ID | Access | What it actually is |
|---|---|---|---|
| `#transit-hubs-aws` | `C0916V8RNS2` | Open | Engineer-to-engineer coordination for AWS Transit Hub: egress-IP allow-listing and firewall-rule requests, CIDR-overlap checks before onboarding a VPC (e.g. AWS Cloud WAN attachments), SIPA/Zscaler Private Access whitelisting questions, and cutover scheduling — heavily featuring the JustGiving CDE (PRD-CDE-VPC) migration. Good source for "why did someone change X" context; not a monitoring feed. |
| `#transit-hub-private` | `C0ABMTC9799` | **Restricted** — invite-only | Working-team channel for transit-hub leads (Amar Goradia, Sampath Mentraddi, Ketan Pantul, Chapara Praveen Kumar) plus Doug Smart and Craig Kozlowski: migration/subscription status reviews, OpsGenie-for-Azure enablement decisions, Zscaler VM tagging (MANA remediation) urgency threads, Tanium Client Edge migration coordination, and Terraform drift investigation (e.g. unexplained Key Vault IP-rule changes found after a PTO gap). Don't assume access, and don't quote its content into any shared artifact — describe its existence and purpose only. |
| `#cm-transit-hubs` | `C0ACT4QT1U7` | Open | Interface to Blackbaud's Change Management team: requesting RFC/CHG scheduling, rescheduling, internal↔external conversion, and closure for transit-hub changes. Ticketing/process only, not technical alert content. |

### Network team — general (not transit-hub-specific)

| Channel | ID | What it actually is |
|---|---|---|
| `#network-team` | `C0A5TDCRQ1F` | The network team's main working channel — standups, retro boards, sprint capacity reports (some auto-generated via a Claude Cowork skill), and RFC announcements ("Starting RFC CHG####...") for changes across the team's full scope, not just transit hub. Broader than the transit-hub-specific channels above. |
| `#network-team-alerts` | `CH08L1GQG` | Automated alert feed (Slackbot), high frequency, all sample messages unlabeled bot posts. Appears to be the network team's general alerting channel — likely broader than transit-hub alerts specifically. Not yet mined for alert-type content; open individual messages before relying on this for a specific alert's meaning. |

### Cloud migration program — Luminate Online (LO)

| Channel | ID | What it actually is |
|---|---|---|
| `#lo-to-public-cloud` | `C079X5KEC06` | The Luminate Online-to-Azure public-cloud migration program channel — daily/near-daily structured status updates (Devin Ehrlich) on storage-latency/NFS root-cause work, FTP timeout bugs, relocation tooling for cluster cutovers (C2/C3), canary testing, and the outbound transactional-mail relay migration off BO3 to Azure. Explicitly touches Transit Hub network/routing design (the S20 subscription) as a dependency. High-value for cloud-migration network questions even though "transit hub" isn't in the name. |
| `#lo-production` | `C197EMF44` | Luminate Online production operations channel — DCM-sourced alerts, ad hoc infra issues (full `/var`, job-status checks), Change-driven patching announcements (CHG####), and DB remediation script coordination across clusters (C2/C3/C8). Operational, not migration-planning; day-to-day LO prod health. |

### Org-wide escalation

| Channel | ID | What it actually is |
|---|---|---|
| `#ops-center` | `CNU2U4NUC` | Blackbaud's IT Operations Center ("OC" / `@SU80D09KK` subteam) — the org-wide first-line channel for escalations: SIRT bridge requests, incident backfill reports (with severity, impact, RFO fields), vendor/AWS-outage contact issues, FirePower IPS deployment confirmations, and password/access resets. Not network-specific, but frequently where a network-adjacent incident first surfaces or where a bridge call gets requested — worth checking during a live, customer-impacting event. |

### Not actually network/cloud-infrastructure channels

| Channel | ID | What it actually is | Why it's flagged |
|---|---|---|---|
| `#engineeringsystem` | `C4FJT1171` | General internal-developer-platform support channel: ADO pipeline issues, GitHub org/repo access requests, SkyUX SPA scaffolding, Service Bus topic problems, environment access. | Not about network/cloud infra at all — it's engineering-tooling support. Don't route a network/transit-hub question here. |
| `#intelligent-platform-group` | `C0BDSS0JT9N` | The Intelligent Platform team's home/people channel — welcomes for new joiners, training-completion reminders, team announcements. | A team/people channel, not a technical or alerting channel. Included only for completeness since it was in the same personal grouping. |

## Practical guidance for /net

- **Active Azure transit-hub alert/incident**: start with the matching `azure-transit-hub-alerts-*`
  channel for the named environment, then check `#azure-transit-hub-pr` for a recent change that might
  explain onset, and `#network-team-alerts` if the issue might be broader than transit hub alone.
- **Active AWS transit-hub alert/incident**: same pattern with `aws-transit-hub-alerts-*` and
  `#aws-transit-hub-pr`, but treat AWS-side alert-type meaning as unverified until sampled the way the
  Azure channels were.
- **"Why was this changed" / "is a change in flight"**: check `#transit-hubs-aws` (AWS) or the relevant
  PR channel, and `#cm-transit-hubs` for the formal RFC/change-request status. `#network-team` for
  broader (non-transit-hub) network changes.
- **Luminate Online / public-cloud migration network questions** (storage, DNS, routing tied to the
  migration): check `#lo-to-public-cloud` first, `#lo-production` for live operational issues.
- **Customer-impacting or needs a bridge call**: check `#ops-center` — that's where SIRT bridges and
  incident backfill get requested org-wide.
- Do not surface `#transit-hub-private` content in any artifact meant for broad sharing — summarize that
  it exists and what kind of discussion happens there, not what was said.
- Do not route network/cloud questions to `#engineeringsystem` or `#intelligent-platform-group` — they
  are not technical sources for this domain despite appearing in the same personal Slack grouping.
- This map is Blackbaud-specific and reflects one point in time (channels can be renamed, archived, or
  have membership change). Treat it as a verified starting point, not a permanent guarantee — re-confirm
  if something here looks stale.
