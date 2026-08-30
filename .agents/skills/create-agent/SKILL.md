---
name: create-agent
description: "Guide the creation of a new HX factory agent: reads governace/templates/agent-checklist.md and walks each step, validating after each. Use when the user says 'create agent', 'new agent', or 'register agent'."
maturity: active
---

# Create Agent

Trigger: 'create agent', 'new agent', 'register agent'

This skill guides the creation of a new HX factory agent. It reads the checklist at governace/templates/agent-checklist.md and walks through each step, validating after each one.

## Workflow

1. Read the checklist from governace/templates/agent-checklist.md
2. Confirm the agent name, family, model lane, and target host with the owner
3. Survey the TKV knowledge directory (be-great)
4. Create the agent directory and files from templates
5. Fill in the profile with all mandatory sections
6. Register the agent across all systems (roster, AGENTS.md, system-mapping, KDD, catalog, manifest)
7. Run validation (render.py + validate.py)
8. Report any missing items

The skill fails closed if any mandatory checklist item cannot be completed. It does not skip steps or create partial registrations.
