---
name: Security-Critical Changes
description: "Use when changing authentication, authorization, security settings, persistence, migrations, proxy or TLS configuration, deployment, media access, or security tests."
applyTo:
  - "app/auth/**"
  - "app/core/config.py"
  - "app/db/**"
  - "app/main.py"
  - "app/media/**"
  - "migrations/**"
  - "docker-compose*.yml"
  - "Dockerfile"
  - "nginx/**"
  - "tests/test_security_controls.py"
---

# Security-Critical Changes

Read [docs/security.md](../../docs/security.md) and the existing tests before
changing security-sensitive behavior. The implemented controls and documented
limitations are the baseline; do not imply this service is a complete identity
platform or certified secure.

- Preserve deny-by-default access: every profile route requires an active
  administrator; PostgreSQL account and role state is authoritative. Redis
  failure must reject authentication rather than bypass it.
- Preserve the last-active-administrator invariant, password reauthentication
  for role changes, credential-version checks, session revocation, and
  non-enumerating login failures. Extend tests when changing these paths.
- Never log or return passwords, raw bearer tokens, credentials, or request
  bodies containing secrets. Never pass passwords as CLI arguments or place
  real secrets in fixtures, examples, snapshots, or test output.
- Do not trust arbitrary forwarded headers. Only use explicitly configured,
  controlled proxy IPs; preserve host validation and production TLS checks.
  Production requires TLS for PostgreSQL and Redis, explicit non-loopback
  hosts, and a trusted proxy configuration.
- Treat the development Compose stack, local passwords, and self-signed
  certificates as development-only. Do not use or target production or
  third-party systems. Run provisioning and performance tests only against
  localhost and a disposable `_test` database.
- Keep media access admin-only and read-only; user uploads and a processing
  worker are not implemented. Do not add unsafe writable mounts or broaden
  supported file types or limits without an explicit design and tests.
- Review migrations for data loss and operational impact. Never run migrations
  or destructive commands against a live or unapproved database; do not remove
  database volumes or existing user data without explicit approval.
- Do not disable or weaken security tests, audit tools, dependency checks, or
  workflow protections to obtain a passing result. Report unresolved findings
  and validation failures explicitly.

See [docs/architecture.md](../../docs/architecture.md) for module boundaries
and [docs/performance.md](../../docs/performance.md) for local-only test
requirements.
