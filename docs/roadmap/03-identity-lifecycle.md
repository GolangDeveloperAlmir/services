# PLAN-03: Identity and account lifecycle

> **Language / Язык:** [English](#english) · [Русский](#russian)
> **Status:** conditional future specification. Current local credentials are for administrators only; end-user self-service, MFA, SSO/OIDC, email verification and recovery are not implemented.

<a id="english"></a>
## English

### Goal and domain separation

Add only identity workflows supported by a confirmed product requirement. Preserve distinct concepts:

| Concept | Responsibility |
| --- | --- |
| Profile | Contact and public attributes approved by the product |
| Identity/account | Login subject, credential or external provider subject, verification state |
| Membership/authorization | Organization membership, role and permission scope |
| Session | Time-bounded authentication result, revoked when account/security state changes |

Profile CRUD must never grant login access or membership automatically.

### Decisions before provider-specific work

Confirm user populations, client applications and required authentication assurance; whether local administrator credentials remain, are replaced by OIDC or coexist under separate policy; whether identity is global or organization-scoped; account linking/unlinking and deprovisioning rules; and an operational owner for the selected identity provider.

### Optional workflows

**MFA:** enrol only after recent authentication; verify factor possession before activation; prefer phishing-resistant authenticators where policy requires; protect recovery codes, enforce one-time use and expiry, rate-limit attempts, audit enrollment/removal and revoke or step-up existing sessions. Never log OTPs or recovery codes.

**OIDC SSO:** use authorization code flow, exact redirect allowlists, cryptographically random state/nonce, issuer/audience/signature/time validation, trusted discovery/JWKS endpoints and approved algorithms. Federated identity is the stable issuer/subject pair, not email alone. Never auto-link accounts solely because email values match. Define provider outage, key rotation, deprovisioning and logout behaviour.

**Email verification and invitations:** use one-time hash-only tokens with purpose binding, expiry, replay protection, resend cooldown and anti-enumeration responses. An invitation must be bound to organization, identity/address, permitted role, inviter, expiry and one-time state; a client parameter must not elevate role. Keep public registration disabled until abuse controls and support are approved.

**Local account recovery:** use random one-time tokens stored as hashes, limited expiry/attempts, account binding, session-version changes and explicit session revocation. Responses must not reveal whether an account exists. Define delivery abuse controls and a manual auditable fallback before implementation.

### Data and API design constraints

Do not replace existing users and local_credentials implicitly. Potential new entities include external provider subjects, MFA factors, recovery credentials, verification challenges, trusted IdP configuration and audit events. Define encryption, uniqueness, cascade, retention and token-minimization through ADR and threat modelling. Never store access/refresh/ID tokens in plaintext or put secrets in query parameters.

Versioned contracts must specify login/challenge/step-up, MFA enrollment and recovery, provider callback/link/unlink, email verification, invitations, recovery consumption, status codes, replay behaviour and rate limits. Exact endpoints wait for UX, provider and API-version decisions.

### Compatibility, testing and acceptance

Preserve the bootstrap CLI until a replacement break-glass procedure is approved. Separate administrator login from end-user login. Do not link accounts by email alone. Test OIDC state/nonce, issuer, audience, signature, expiry, redirect manipulation, JWKS rotation/outage and replay; MFA replay/races/brute force/recovery; invitation and recovery enumeration/expiry/parallel consumption; session revocation on password/factor/provider/membership changes; and absence of secrets/PII in logs and traces.

Acceptance requires an approved use case and threat model for every feature, stable federated identity, proof of account ownership for linking, recovery that cannot bypass tenant/RBAC/MFA policy, hash-only secret storage, one-time/expiry/rate-limit/replay protections, tested revocation and support runbooks. Obtain independent security review before a public external-authentication launch.

---

<a id="russian"></a>
## Русский

### Цель и разделение домена

Добавлять только те identity workflows, которые подтверждены продуктовыми требованиями. Сохранять отдельные понятия:

| Понятие | Ответственность |
| --- | --- |
| Profile | Контактные и публичные атрибуты, разрешённые продуктом |
| Identity/account | Субъект входа, credential или внешний provider subject, состояние верификации |
| Membership/authorization | Членство в организации, роль и область разрешений |
| Session | Ограниченный по времени результат аутентификации, отзываемый при изменении account/security state |

CRUD профилей никогда не должен автоматически выдавать право входа или membership.

### Решения до provider-specific разработки

Подтвердить аудитории и клиентские приложения, требуемый уровень assurance; сохраняются ли локальные admin credentials, заменяются OIDC или работают вместе по отдельной политике; является identity глобальной или organization-scoped; правила linking/unlinking и deprovisioning; владельца эксплуатации выбранного identity provider.

### Возможные workflows

**MFA:** enrollment только после недавней аутентификации; доказать владение фактором до активации; предпочитать phishing-resistant authenticators, если того требует политика; защищать recovery codes, обеспечивать одноразовость и expiry, ограничивать попытки rate limit, аудировать подключение/удаление и отзывать либо step-up существующие сессии. OTP и recovery codes запрещено логировать.

**OIDC SSO:** применять authorization code flow, точный allowlist redirect URI, криптографически случайные state/nonce, проверки issuer/audience/signature/time, доверенные discovery/JWKS endpoints и утверждённые алгоритмы. Федеративная identity определяется устойчивой парой issuer/subject, а не одним email. Нельзя связывать аккаунты автоматически только из-за совпадения email. Нужно определить outage provider, ротацию ключей, deprovisioning и поведение logout.

**Email verification и приглашения:** использовать одноразовые hash-only токены с привязкой к назначению, expiry, replay protection, cooldown повторной отправки и anti-enumeration responses. Invitation связывается с организацией, identity/address, разрешённой ролью, inviter, expiry и одноразовым состоянием; параметр клиента не должен повышать роль. Публичную регистрацию не включать до утверждения abuse controls и поддержки.

**Восстановление локального аккаунта:** случайные одноразовые токены хранить только в виде hash, ограничить TTL/попытки, привязать к аккаунту, менять session version и явно отзывать сессии. Ответы не должны раскрывать существование аккаунта. До реализации утвердить анти-abuse меры доставки и ручной auditable fallback.

### Ограничения данных и API

Не заменять существующие users и local_credentials неявно. Возможные сущности: внешние provider subjects, MFA factors, recovery credentials, verification challenges, trusted IdP configuration и audit events. Правила encryption, uniqueness, cascade, retention и минимизации токенов утверждаются через ADR и threat model. Access/refresh/ID tokens нельзя хранить в plaintext, секреты нельзя передавать через query parameters.

Версионируемый контракт должен описывать login/challenge/step-up, MFA enrollment/recovery, provider callback/link/unlink, email verification, invitations, recovery consumption, status codes, replay behaviour и rate limits. Конкретные endpoints определяются после выбора UX, provider и версии API.

### Совместимость, тестирование и критерии приёмки

Сохранять bootstrap CLI, пока не утверждена альтернативная break-glass процедура. Разделять admin login и end-user login. Не связывать аккаунты по одному email. Проверять OIDC state/nonce, issuer, audience, signature, expiry, redirect manipulation, JWKS rotation/outage и replay; MFA replay/races/brute force/recovery; enumeration/expiry/parallel consumption для invitation и recovery; отзыв сессий при смене password/factor/provider/membership; отсутствие секретов/PII в logs и traces.

Приёмка требует утверждённый use case и threat model для каждой функции, устойчивую federated identity, доказательство владения при linking, recovery без обхода tenant/RBAC/MFA, hash-only хранение секретов, проверенные одноразовость/expiry/rate limit/replay protections и session revocation, support runbooks. До публичного запуска внешней аутентификации провести независимый security review.
