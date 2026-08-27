# Kimi Code → OmniRoute Provider Setup

**Status:** reference, owner-approved 2026-08-27; implementation deferred until baseline platform deployment completes (owner sequencing, state-log row 43).
**Purpose:** run Kimi Code sessions through the OmniRoute gateway (hxs-8) instead of a direct cloud provider — every call logged and metered in the gateway, local fleet models first-class, external models (OpenRouter) opt-in per session.

---

## 1. Create a dedicated client key (owner, dashboard)

Do **not** reuse the root ops key (`/opt/omniroute/ops/.hx-client-key` — governor artifact).

1. Open `http://192.168.50.207:20128`, sign in (password-only, SSH parity).
2. API Keys → create key, name it `kimi-code-hxsa`, default scopes.
3. Copy it immediately — it is shown once. This becomes `<HX_CLIENT_KEY>` below.

## 2. Append to `/home/hxsa/.kimi-code/config.toml`

Append this block verbatim, replacing only `<HX_CLIENT_KEY>`. Do **not** change `default_model` — kimi-k3 stays the default; these models are per-session opt-in.

```toml
# ── HX OmniRoute gateway (hxs-8) ─────────────────────────────────
[providers.omniroute]
type = "openai"
base_url = "http://192.168.50.207:20128/v1"
api_key = "<HX_CLIENT_KEY>"

# Local fleet (64K operating profile — gateway advertises 128000, capped on purpose)
[models."omniroute/qwen-x"]
provider = "omniroute"
model = "ollama-local/hx-qwen3.8-27b-64k:latest"
max_context_size = 65536
capabilities = [ "thinking", "tool_use" ]

[models."omniroute/coder-x"]
provider = "omniroute"
model = "ollama-local/hx-qwen3.6-coderx-64k:latest"
max_context_size = 65536
capabilities = [ "thinking", "tool_use" ]

[models."omniroute/meta-x"]
provider = "omniroute"
model = "ollama-local/hx-muse-glimmer-64k:latest"
max_context_size = 65536
capabilities = [ "thinking", "tool_use" ]

# External: ZAI GLM-5.3 Flash via OpenRouter (spends OR credits if paid — cap first)
[models."omniroute/glm-5.3-flash"]
provider = "omniroute"
model = "openrouter/z-ai/glm-5.3-flash"
max_context_size = 131072
capabilities = [ "thinking", "tool_use" ]
```

Model IDs verified against the live gateway catalog 2026-08-27 (`GET /v1/models`, 1497 entries).

## 3. Permissions

`chmod 600 /home/hxsa/.kimi-code/config.toml` (it already holds the Moonshot key; the HX key is equally sensitive — it can spend through the gateway).

## 4. Use it (per session, nothing global changes)

- In the TUI: `/model` → pick `omniroute/qwen-x`, `omniroute/coder-x`, `omniroute/meta-x`, or `omniroute/glm-5.3-flash`.
- First test: give the session a small bounded task, then confirm the calls appear in OmniRoute's usage log (dashboard → Logs/Usage) — that proves the route.

## 5. Rollback

`/model` back to `moonshot-ai/kimi-k3`, or remove the block. No other state is touched.

## Notes and cautions

- **LAN-only:** the gateway is `192.168.50.207` — this provider only works on the HX network.
- **Cost:** local models (qwen-x / coder-x / meta-x) are free to run; `glm-5.3-flash` bills against the owner's OpenRouter account if it is a paid model — set the OR spend cap before letting an agent session use it heavily.
- **Data posture:** local-model sessions stay on the fleet (local-first rule satisfied mechanically); `glm-5.3-flash` prompts leave the network and are retained by the provider (not used for training, per its terms).
- **Governor exception stands:** the owner's rule keeps Kimi-K3 as the governor brain; this setup is for worker sessions and post-baseline evaluation.
