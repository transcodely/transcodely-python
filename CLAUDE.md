# Transcodely Python SDK

`transcodely` (PyPI) — the official Python SDK, generated from the api repo's public
protos (`buf generate` → `src/transcodely/v1/*_pb2.py(i)`) with hand-written Stripe-style
resource namespaces in `src/transcodely/resources/`. Wire format is snake_case JSON +
simplified lowercase enums (a port of the api repo's `internal/connect/codec.go`, in
`src/transcodely/_codec/json_codec.py`). Upstream (`../api`) is authoritative for
wire/enum/error behavior.

- Regenerate from proto: `./scripts/sync-protos.sh && buf generate`
- Build / test: `python -m build` · `pytest`

## Docs are the contract (drift)

The public docs (`transcodely/web` → `src/routes/(docs)/docs/**`, especially
`getting-started/sdks/python` and the per-resource SDK method maps such as the one in
`api-reference/webhooks`) document this SDK's exact public surface — including exact
kwarg names on every resource method. Rules:

- Any public-surface change (methods, kwargs, enum-string handling, webhook event
  types, exception classes) must be mirrored in those web docs pages **in the same
  release window**. Web's mechanical drift gate validates proto-level facts but does
  NOT parse `python` code fences — whoever changes this SDK owns the docs snippets.
- Before renaming/removing anything public, grep the web repo's docs for usages
  (` ```python ` fences calling `client.<resource>.<method>(...)`); docs may also
  reference capabilities that shipped here first (docs kwargs are the target
  signature — the 2026-07 `jobs.create()` extension exists because docs led the SDK).
- Watch the `opts=` split: fixed-signature methods (jobs, webhook_endpoints, health,
  list/get) accept `opts=`; bare-`**kwargs` create/update methods (presets, origins,
  organizations, api_keys, apps, videos) do NOT — keep docs examples consistent with
  the signature that actually exists.
- Vendored proto comments flow into generated `.pyi` stubs and docs — when resyncing,
  take the api repo's comments verbatim (they are maintained as public documentation
  there).

---

## TODO: surface `disable_audio` + single-variant streaming presets

Upstream API changes this SDK still needs to expose (api PR #119, worker PR #57).

### What changed in the API
1. **`disable_audio` (video-only output).** New field:
   - `OutputSpec.disable_audio` — `optional bool`, override semantics: when unset
     it inherits the referenced preset's value; `true` drops audio for that output.
   - `Preset.disable_audio` (`bool`) plus `CreatePresetRequest` / `UpdatePresetRequest`.
   - Wire name is snake_case `disable_audio`. The server rejects `disable_audio: true`
     combined with explicit `audio[]` tracks (`parameter_invalid`).
   - Pricing is unchanged (no audio cost component).
2. **Graceful no-audio sources.** A source video with no audio track no longer fails
   packaging — it now produces a valid video-only output automatically (worker PR #57).
   No SDK code change; worth a line in the README / audio docs.
3. **Single-variant streaming presets.** The API dropped the "minimum 2 ABR variants"
   rule, so a single-variant HLS/DASH/CMAF preset is now valid (e.g. one vertical 720p
   HLS stream). No proto change — just relax any client-side mirror and update examples.

### Work items
- [x] `./scripts/sync-protos.sh && buf generate` — DONE: `disable_audio` is present on
      `job_pb2.OutputSpec` / `preset_pb2.Preset` (verified 2026-07-15). The resource methods take
      `outputs` as dicts, so pass `outputs=[{"type": "hls", "video": [...], "disable_audio": True}]`.
- [ ] Add an `examples/` demo creating a video-only output (and/or a single-variant
      streaming preset).
- [ ] Add a pytest asserting it round-trips as `"disable_audio": true` through the json
      codec (follow the existing `_codec` tests).
- [ ] Update `README.md` + `CHANGELOG.md` (release-please) when it lands.
- [ ] Blocked on api PR #119 (proto) merging first.

Refs: transcodely/api#119, transcodely/worker#57.
