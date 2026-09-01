# bbi-ai-skills

Internal Blackbaud repository for custom Claude Skills. Use this repo to download a skill someone else
built, or to upload/update one you've built, so the team can share and reuse them.

## Layout

Skills live under `Claude/<skill-name>/`, matching the folder structure Claude's skill system expects:

```
Claude/<skill-name>/
  SKILL.md              # required — YAML frontmatter (name, description) + instructions
  references/            # optional — reference docs the skill reads on demand
  scripts/                # optional — code the skill can execute
```

## Importing a skill to your own machine (e.g. `net`)

1. Pull or download this repo so you have `Claude/net/` locally (via `git clone`, `git pull`, or
   downloading the folder from GitHub).
2. In Claude Code, Cowork, or claude.ai, add the skill by pointing it at (or copying in) the
   `Claude/net/` folder exactly as-is — `SKILL.md` should sit at the top level of what you import,
   with `references/` and `scripts/` as siblings, not nested under another folder. If your setup
   requires a zip instead of a folder, zip the **contents** of `Claude/net/` (so `SKILL.md` is at the
   zip root) and upload that zip.
3. Once imported, invoke it as `/net` (or however your Claude setup surfaces skill names) for network
   incident troubleshooting or AWS/Azure architecture design work.
4. No further setup is required for the general skill logic. One caveat: `net` ships with a
   Blackbaud-specific Slack channel map (`Claude/net/references/blackbaud-cloud-channels.md`) built from
   one engineer's own Slack sidebar grouping — channel names are stable across Blackbaud Slack, but if
   you don't have access to a given channel, or a channel has since been renamed/archived, treat that
   file as a starting point to verify rather than a guarantee. It has no effect outside a Blackbaud
   Slack context.

## Skills in this repo

### `Claude/net`

Senior network incident engineer / cloud network architect skill. Four independently invocable phases:

- **Phase 0** — AWS/Azure architecture design (Well-Architected, landing zones, HLD/LLD, migration, VPC/VNet design).
- **Phase 1** — Ingest, scope and triage an active or reported network issue into a hypothesis-driven roadmap.
- **Phase 2** — Active diagnosis via Azure CLI, AWS CLI, Cisco IOS/IOS-XE, Cisco ASA/FTD, Palo Alto, Citrix NetScaler/ADC, Cisco Meraki, and host-level Windows/Linux checks (including no-admin techniques and bandwidth tests).
- **Phase 3** — Technical/executive summaries and a canonical Excel incident workbook, kept updated in place rather than duplicated.

Bundles a Python client-network-agent runtime (`scripts/client_network_agent/`) for one-shot end-host evidence collection (DNS, TCP, HTTP, OS-native commands) — see `Claude/net/references/client-network-agent.md` for usage.

Also bundles `Claude/net/references/blackbaud-cloud-channels.md`, a verified directory of the Slack
channels behind Blackbaud's AWS/Azure transit-hub work, the network team, and related cloud-migration
programs — keyed by channel name (never by a personal Slack sidebar category, since that grouping is
per-user and doesn't transfer between people) so any Blackbaud user importing this skill benefits from
it regardless of how they've organized their own sidebar.

## Adding a new skill

1. Create `Claude/<new-skill-name>/SKILL.md` with YAML frontmatter (`name`, `description` — max 1024 characters).
2. Add any `references/` or `scripts/` the skill needs.
3. Update this README's skill list.
4. Commit and push.
