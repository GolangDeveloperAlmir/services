# Guidance for AI Agents

This file is the shared project context for coding agents. Treat the checked-in
code and current tests as the source of truth; a roadmap item is not an
implemented feature or a delivery commitment.

## Project boundaries

- This is a FastAPI profile service for controlled administrator use, not a
  public identity platform. Every `/users` endpoint is restricted to an active
  administrator. Do not silently add end-user access, tenant isolation, MFA,
  SSO/OIDC, password recovery, or other identity features outside the issue's
  scope.
- Profile creation does not create credentials or grant roles. The only
  built-in role is `admin`.
- `app.main` composes the application; `app.auth` owns local credentials,
  sessions, and authorization; `app.users` owns profile API and business
  rules; `app.db` owns persistence; `app.core` owns shared configuration,
  logging, and telemetry. Preserve the dependency rules in
  [docs/architecture.md](docs/architecture.md).
- PostgreSQL is authoritative for account and role state. Redis holds
  ephemeral sessions and rate counters; Redis failure must never grant access
  or trigger an unauthenticated fallback.
- The web console keeps its bearer token in tab memory. Browser-local media
  is not uploaded; there is no media upload endpoint or processing worker.
  Keep the curated media catalog read-only and admin-only.
- Compose, self-signed certificates, and example credentials are for local
  development only. Do not present them as production deployment settings.

## Security and safety requirements

- Read [docs/security.md](docs/security.md) before changing authentication,
  authorization, settings, database models or migrations, proxy/TLS behavior,
  deployment configuration, media access, or security tests. Follow
  [.github/instructions/security.instructions.md](.github/instructions/security.instructions.md)
  for those files.
- Preserve deny-by-default authorization and existing account invariants,
  especially protection of the last active administrator, password
  reauthentication for role changes, session revocation, and generic login
  failures. Add regression tests for security-sensitive behavior.
- Never print, copy into patches, commit, or expose `.env` contents, tokens,
  private keys, certificates, production data, or other credentials. Use only
  placeholders in examples. Do not read local secret files unless the task
  explicitly requires it; even then, avoid displaying their values.
- Never run commands, performance tests, migrations, provisioning, scans, or
  load against production, third-party, or otherwise unapproved systems.
  Performance tests and provisioning are local-only and require a disposable
  `_test` database; see [docs/performance.md](docs/performance.md).
- Do not weaken security controls, bypass failing checks, or broaden proxy,
  host, network, or filesystem trust just to make a test pass. Do not delete
  data, volumes, certificates, or user changes without explicit approval.
- Do not add media unless its usage rights are verified. Preserve third-party
  license notices and the repository's attribution requirements in
  [LICENSE](LICENSE).

## Implementation and verification

- Keep changes focused. Inspect the relevant implementation and tests first;
  preserve unrelated worktree changes. Use existing patterns and helpers,
  typed interfaces, and explicit error handling. Do not swallow errors or
  return success-shaped fallbacks.
- Add or update tests and documentation for behavior changes. Keep Russian and
  English user-facing documentation in sync where both sections exist.
- For API/schema changes, regenerate and commit `openapi.yaml` with
  `make openapi`; validate with `make validate-specs`. For frontend source
  changes, run `make frontend-check` and `make frontend-build`, and commit the
  generated `frontend/public/assets/app.js`.
- Use Python 3.14 and `uv`. Run the narrowest relevant checks; the documented
  commands include `make test`, `make lint`, `make architecture`,
  `make validate-specs`, `make security`, and `make check`. Frontend checks
  require `make frontend-install`; `make check` includes security and frontend
  checks. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow.
- If dependency manifests change, regenerate the applicable lockfile
  (`uv.lock` or `frontend/package-lock.json`) and run the relevant checks.
- Before finishing, review the diff for unrelated edits, generated files,
  secrets, broken documentation links, and whitespace errors. Report commands
  run and checks not run; do not claim unrun checks passed.

## Further context

- [README.md](README.md): scope, setup, and user-facing behavior.
- [docs/index.md](docs/index.md): documentation map.
- [CONTRIBUTING.md](CONTRIBUTING.md): development and review workflow.
- [SECURITY.md](SECURITY.md): private vulnerability reporting.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): community expectations.
- [SUPPORT.md](SUPPORT.md): support channels and public-reporting cautions.
