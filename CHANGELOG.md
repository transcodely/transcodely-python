# Changelog

All notable changes to the Transcodely Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Breaking changes are allowed on minor bumps until 1.0.0.

## [0.1.2](https://github.com/transcodely/transcodely-python/compare/v0.1.1...v0.1.2) (2026-07-02)


### Features

* **origins:** add Cloudflare R2 as a first-class provider ([#4](https://github.com/transcodely/transcodely-python/issues/4)) ([d01c2af](https://github.com/transcodely/transcodely-python/commit/d01c2af2e0cafa32e4cb68213bebaf00eaa65c2f))
* sync proto — thumbnail path_template + accumulated drift ([#5](https://github.com/transcodely/transcodely-python/issues/5)) ([cffc367](https://github.com/transcodely/transcodely-python/commit/cffc367524ba4bda374be8f528e20533cf2b040c))

## [0.1.1](https://github.com/transcodely/transcodely-python/compare/v0.1.0...v0.1.1) (2026-05-05)


### Features

* initial 0.1.0 alpha release ([25da9b2](https://github.com/transcodely/transcodely-python/commit/25da9b2cdbf46ee6225babbacb5a5616a50d6070))

## [0.1.0] — Alpha

Initial public alpha. Sync-only client; async support is planned for a later release. Covers 100% of the public RPC surface (56 RPCs across 10 services). Stripe-style facade: lazy resource namespaces, auto-pagination via `auto_paging_iter()`, auto-idempotency on `create` mutations, typed exception hierarchy (1 base + 8 concrete), Watch streams with auto-reconnect, calendar-versioned API.
