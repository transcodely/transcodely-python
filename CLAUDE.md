# Transcodely Python SDK

`transcodely` (PyPI) — the official Python SDK, generated from the api repo's public
protos (`buf generate` → `src/transcodely/v1/*_pb2.py(i)`) with hand-written Stripe-style
resource namespaces in `src/transcodely/resources/`. Wire format is snake_case JSON +
simplified lowercase enums (a port of the api repo's `internal/connect/codec.go`, in
`src/transcodely/_codec/json_codec.py`). Upstream (`../api`) is authoritative for
wire/enum/error behavior.

- Regenerate from proto: `./scripts/sync-protos.sh && buf generate`
- Build / test: `python -m build` · `pytest`

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
- [ ] `./scripts/sync-protos.sh && buf generate` — `disable_audio` then appears on
      `job_pb2.OutputSpec` / `preset_pb2.Preset` automatically. The resource methods take
      `outputs` as dicts, so pass `outputs=[{"type": "hls", "video": [...], "disable_audio": True}]`.
- [ ] Add an `examples/` demo creating a video-only output (and/or a single-variant
      streaming preset).
- [ ] Add a pytest asserting it round-trips as `"disable_audio": true` through the json
      codec (follow the existing `_codec` tests).
- [ ] Update `README.md` + `CHANGELOG.md` (release-please) when it lands.
- [ ] Blocked on api PR #119 (proto) merging first.

Refs: transcodely/api#119, transcodely/worker#57.
