# Changelog

All notable changes to the Transcodely Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Breaking changes are allowed on minor bumps until 1.0.0.

## [0.3.1](https://github.com/transcodely/transcodely-python/compare/v0.3.0...v0.3.1) (2026-07-15)


### Features

* **resources:** match the documented public surface ([#19](https://github.com/transcodely/transcodely-python/issues/19)) ([4eb4110](https://github.com/transcodely/transcodely-python/commit/4eb411056b78742d92dc5a7c78478ff0812f7aee))

## [0.3.0](https://github.com/transcodely/transcodely-python/compare/v0.2.0...v0.3.0) (2026-07-15)


### ⚠ BREAKING CHANGES

* App.webhook, CreateAppRequest.webhook, and UpdateAppRequest.webhook (WebhookConfig / CreateWebhookConfig / UpdateWebhookConfig) are removed; the proto field numbers/names are now reserved. App-level webhook configuration is superseded by the WebhookService endpoints API, already exposed in this SDK as client.webhook_endpoints (create / retrieve / update / delete / list / rotate_secret / send_test / list_deliveries / get_health) with signature-verification helpers under client.webhooks. The three removed types are dropped from transcodely.types imports and __all__.

### Features

* sync protos — explicit app scoping; remove legacy app webhook config ([#15](https://github.com/transcodely/transcodely-python/issues/15)) ([9784930](https://github.com/transcodely/transcodely-python/commit/9784930122a899fa60469b687c51d85d7ac987bc))

## [0.2.0](https://github.com/transcodely/transcodely-python/compare/v0.1.3...v0.2.0) (2026-07-12)


### ⚠ BREAKING CHANGES

* `Event.livemode` is removed and API keys no longer carry an environment (no `ak_test_`/`ak_live_` distinction).

### Features

* proto resync — rotation metadata + measured output metrics ([#11](https://github.com/transcodely/transcodely-python/issues/11)) ([e5fa0e8](https://github.com/transcodely/transcodely-python/commit/e5fa0e8d85adabd296cb362cd6d419c1bb735e48))
* remove API-key environment and webhook livemode ([#13](https://github.com/transcodely/transcodely-python/issues/13)) ([0b68641](https://github.com/transcodely/transcodely-python/commit/0b68641fc7508c55114eae78ec9d99269ef91312))
* **webhooks:** add signature verification and endpoint/event resources ([#10](https://github.com/transcodely/transcodely-python/issues/10)) ([e742828](https://github.com/transcodely/transcodely-python/commit/e742828d6ce91ec8cc16d82ee6bc1982a5787a94))


### Documentation

* commit CLAUDE.md (was untracked — the routine fleet reads it via the GitHub API) ([b2a843e](https://github.com/transcodely/transcodely-python/commit/b2a843e64e3589f3adbbb86fc1c4a5b5ef85cfda))

## [0.1.3](https://github.com/transcodely/transcodely-python/compare/v0.1.2...v0.1.3) (2026-07-07)


### Documentation

* **examples:** add S3-compatible (custom-endpoint) origin example ([#7](https://github.com/transcodely/transcodely-python/issues/7)) ([bfc1ee5](https://github.com/transcodely/transcodely-python/commit/bfc1ee5dfd6ac1803b9e94f4aaf3ada71421724a))

## [0.1.2](https://github.com/transcodely/transcodely-python/compare/v0.1.1...v0.1.2) (2026-07-02)


### Features

* **origins:** add Cloudflare R2 as a first-class provider ([#4](https://github.com/transcodely/transcodely-python/issues/4)) ([d01c2af](https://github.com/transcodely/transcodely-python/commit/d01c2af2e0cafa32e4cb68213bebaf00eaa65c2f))
* sync proto — thumbnail path_template + accumulated drift ([#5](https://github.com/transcodely/transcodely-python/issues/5)) ([cffc367](https://github.com/transcodely/transcodely-python/commit/cffc367524ba4bda374be8f528e20533cf2b040c))

## [0.1.1](https://github.com/transcodely/transcodely-python/compare/v0.1.0...v0.1.1) (2026-05-05)


### Features

* initial 0.1.0 alpha release ([25da9b2](https://github.com/transcodely/transcodely-python/commit/25da9b2cdbf46ee6225babbacb5a5616a50d6070))

## [0.1.0] — Alpha

Initial public alpha. Sync-only client; async support is planned for a later release. Covers 100% of the public RPC surface (56 RPCs across 10 services). Stripe-style facade: lazy resource namespaces, auto-pagination via `auto_paging_iter()`, auto-idempotency on `create` mutations, typed exception hierarchy (1 base + 8 concrete), Watch streams with auto-reconnect, calendar-versioned API.
