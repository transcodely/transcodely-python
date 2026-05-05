# Changelog

All notable changes to the Transcodely Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Breaking changes are allowed on minor bumps until 1.0.0.

## [0.1.0] — Alpha

Initial public alpha. Sync-only client; async support is planned for a later release. Covers 100% of the public RPC surface (56 RPCs across 10 services). Stripe-style facade: lazy resource namespaces, auto-pagination via `auto_paging_iter()`, auto-idempotency on `create` mutations, typed exception hierarchy (1 base + 8 concrete), Watch streams with auto-reconnect, calendar-versioned API.
