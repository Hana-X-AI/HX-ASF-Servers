# Agent Creation Checklist

This checklist is MANDATORY for every new agent. Do not skip steps. Validate after each step. Fail closed if a step cannot be completed.

## Pre-creation

- [ ] 1. Survey TKV knowledge directory using be-great skill (identify the specific /opt/tkv-local/ path for this agent's domain)
- [ ] 2. Confirm owner directive or governor work order authorizes the agent
- [ ] 3. Confirm model lane assignment (owner decision)
- [ ] 4. Confirm target host and system assignment from system-mapping

## File creation

- [ ] 5. Create agents/<name>/ directory
- [ ] 6. Create charter.md from template (governace/templates/agent/charter.md)
- [ ] 7. Create profile.md from template (governance/templates/agent/profile.md)

## Profile mandatory sections

- [ ] 8. Identity table includes: Name, Role, Family, Class, Reports to, Ultimate owner, Environment, Default mode, Certification authority, Model lane, Verifier, Activation status
- [ ] 9. TKV knowledge directory pointer (specific /opt/tkv-local/ path, NOT generic)
- [ ] 10. be-great standing directive (mandatory: 'survey TKV before acting')
- [ ] 11. SSH credential handling section (grep-only extraction, askpass pattern, never source/eval, never Read tool on .local.env)
- [ ] 12. Skills available section (be-great, eli5, bro, wait-what, quick, human, corp, copy)
- [ ] 13. Provenance section

## Registration

- [ ] 14. Add to agents/README.md roster table
- [ ] 15. Add to AGENTS.md family taxonomy table
- [ ] 16. Add to AGENTS.md per-agent model lanes (labeled correction if existing lane is superseded)
- [ ] 17. Add to servers/system-mapping.md (S<N> row in target-state table + new agents table)
- [ ] 18. Add to servers/SERVER-REGISTRY.md if host-bound (with labeled correction if stale)
- [ ] 19. Create KDD registration document at governace/decisions/KDD-<NNNN>-<name>-registration.md
- [ ] 20. Add KDD to scripts/wiki/manifest.txt
- [ ] 21. Create catalog records: knowledge/catalog/documents/DOC-agent-<name>-charter.yaml and DOC-agent-<name>-profile.yaml
- [ ] 22. Create catalog record: knowledge/catalog/documents/DOC-kdd-<NNNN>-<name>-registration.yaml
- [ ] 23. Add all 3 catalog records to knowledge/catalog/index.yaml

## Verification

- [ ] 24. Verify model lane via OmniRoute (if cloud lane: curl models endpoint, confirm model in catalog; if local lane: confirm Ollama serving)
- [ ] 25. Run python3 scripts/wiki/render.py — all manifest docs in sync
- [ ] 26. Run python3 scripts/validate.py — must be 4/4 PASS
- [ ] 27. Commit

## Post-creation hook

The agent-creation-check.sh hook (scripts/hooks/) fires automatically on Write|Edit to agents/ and warns if any checklist items are missing.
