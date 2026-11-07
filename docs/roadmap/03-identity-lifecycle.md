# 03. Identity и жизненный цикл аккаунта

> **Статус:** условное будущее ТЗ (`PLAN-03`). Сегодня локальные credentials
> предназначены для администраторов; пользовательского self-service, MFA,
> SSO/OIDC, подтверждения email и recovery flow нет. Не считать изложенное
> текущей функцией.

## 1. Цель

Добавить только те пользовательские identity workflows, которые подтверждены
продуктом, при сохранении чёткого разделения:

- **Profile:** контактные/публичные атрибуты, разрешённые владельцем.
- **Identity/account:** способ входа, статус верификации, credentials или
  внешний provider subject.
- **Membership/authorization:** организации, роли, разрешения и их срок
  действия.
- **Session:** ограниченный по времени результат аутентификации, который
  отзывается при изменении account/security state.

Profile CRUD не должен автоматически выдавать право входа или членство.

## 2. Варианты и рекомендуемый порядок решений

1. Подтвердить субъектов, входящие приложения, требуемые assurance level и
   обязательность MFA.
2. Согласовать, остаются ли локальные admin credentials, заменяются OIDC или
   поддерживаются одновременно с раздельной политикой.
3. Решить, распространяется ли identity глобально между организациями или
   имеет отдельную связь в каждой организации; учесть `PLAN-02`.
4. Определить linking/unlinking, reauthentication, account suspension,
   deprovisioning и удаление данных.
5. Выбрать OIDC provider capability и operational owner до написания
   provider-specific кода.
6. Только после этого реализовывать соответствующие функции — не обязательно
   весь список ниже.

## 3. Возможные функциональные потоки

### 3.1 MFA

Если политика требует MFA, спроектировать:

- enrolment только после свежей аутентификации; повторная проверка перед
  привилегированной операцией;
- набор допустимых методов и assurance requirements (например,
  phishing-resistant authenticator как предпочтительная цель; TOTP как
  fallback только при утверждении);
- подтверждение фактического владения фактором до его активации;
- безопасное хранение секретов recovery codes/факторов, однократное
  использование и немедленное invalidation после потребления;
- отзыв/перепривязку фактора через recovery flow, защищённый от social
  engineering;
- ограничения brute-force, аудит включения/удаления, уведомление пользователя
  и отзыв либо step-up существующих сессий.

Не отправлять OTP или recovery code в application logs, traces, analytics,
audit payload, URL или support ticket.

### 3.2 OIDC SSO

Предлагаемый authorization-code flow должен:

- применять TLS и точный allowlist redirect URI; не использовать wildcard
  callback;
- генерировать и проверять криптографически стойкие `state` и `nonce`;
- проверять issuer, audience/client, подпись, временные claims, допустимый
  алгоритм и необходимые scopes; доверять только заранее настроенным
  discovery/JWKS endpoints;
- моделировать provider identity по устойчивой паре `(issuer, subject)`, а
  не по изменяемому email;
- не создавать автоматически связь с локальным аккаунтом лишь потому, что
  email совпал; linking требует подтверждённого владения обеими сторонами или
  управляемого invitation flow;
- ограничивать разрешённые issuer/tenant и задавать безопасное поведение при
  недоступном provider/JWKS, ротации ключей и отзыве пользователя;
- вести аудит изменения конфигурации provider без хранения токенов и
  assertion.

Импорт групп/ролей из provider не должен давать привилегию без явной,
проверяемой mapping policy. Решить, применяются ли provider-initiated logout
и back-channel logout; не обещать глобальный logout, если клиентские сессии
нельзя отозвать.

### 3.3 Подтверждение адреса и приглашение

Если email используется для связи/входа:

- отправка подтверждения только после безопасного создания/изменения адреса;
- одноразовый токен с hash-only хранением, ограниченным TTL, purpose binding
  и защитой от replay;
- одинаково безопасные ответы, не раскрывающие существование учётной записи;
- rate limiting, resend cooldown, защита от enumeration и abuse email;
- изменение адреса не становится активным до подтверждения; определить
  поведение старых сессий и уведомление старого/нового адреса;
- invitation token привязан к организации, адресу/identity, допустимой роли,
  inviter, сроку и одноразовому состоянию; нельзя расширить роль параметром
  клиента.

Публичная регистрация остаётся выключенной, пока владелец продукта не
утвердит abuse model, квоты, anti-automation и поддержку.

### 3.4 Восстановление локального доступа

Recovery flow должен быть безопаснее простого сброса по email:

- не раскрывать, существует ли адрес/аккаунт;
- использовать случайный одноразовый token, хранить только hash, привязать к
  аккаунту и операции, ограничить время и число попыток;
- отозвать/обновить token после использования, изменить session version и
  определить, какие активные сессии отзываются;
- уведомлять о запросе и успешной смене без раскрытия секрета;
- ограничить частоту по нескольким ключам и не позволять массово рассылать
  письма; настроить доставку, bounce/abuse и incident ownership;
- иметь ручную, auditable процедуру восстановления, если email/provider
  недоступен.

До согласования почтового провайдера, доказательства владения, privacy,
rate limits и поддержки recovery не внедрять.

## 4. Предварительные модели данных и API

Существующие `users` и `local_credentials` не должны автоматически заменяться.
Для обсуждения могут потребоваться отдельные сущности/атрибуты:

- внешний credential: provider/issuer, subject, user reference, timestamps;
- факторы MFA и одноразовые recovery credentials;
- verification/recovery challenges с hash, purpose, expiry, consumption state;
- конфигурация доверенных IdP с владельцем/статусом;
- audit событий по security state changes.

Это не утверждённая схема: хранение, шифрование, уникальность, cascade,
retention и раздельное управление provider credentials требуют ADR и threat
model. Не хранить access/refresh/ID token в открытом виде; если использование
provider tokens действительно необходимо, отдельно определить минимизацию,
шифрование, срок жизни и отзыв.

Версионированный API-контракт должен описывать:

- login/challenge/step-up и session assurance;
- MFA enrollment, verification, disable и recovery;
- provider callback/link/unlink и безопасные ошибки;
- email verification, invitation accept/revoke/expire;
- recovery request/consume без enumeration;
- status codes, replay behavior, rate limits и события аудита.

Конкретные URL и JSON payload не фиксируются до выбора UX, IdP и версии API.
Секреты не помещать в query parameters.

## 5. Совместимость и переход

- Сохранить bootstrap CLI для первого локального системного администратора,
  пока не согласован альтернативный break-glass путь.
- Развести admin login policy и end-user login policy; не ослаблять текущие
  требования ради удобства перехода.
- Разрешить ограниченный dual-auth период только с явными датами и способом
  отключения устаревающего flow.
- Провести инвентаризацию локальных credentials, provider identity collision
  и непроверенных email; не связывать записи автоматом по email.
- Проверить отзыв Redis-сессий, смену `session_version` и поведение при
  недоступности provider, Redis и почтовой доставки.
- Не выпускать recovery/MFA без соответствующих поддержки, incident
  playbooks и сценария потери фактора.

## 6. Security/privacy тестирование

- OIDC: некорректные `state`/`nonce`, replay, wrong issuer/audience,
  expired/future claims, подпись/algorithm mismatch, JWKS rotation/outage,
  redirect manipulation, callback replay.
- Linking: совпавший email без подтверждения, чужой subject, повторная
  привязка, удалённый provider account, конфликт issuer/subject.
- MFA: повторный/просроченный код, race при consumption, перебор, повторное
  enrollment, потеря/отзыв фактора и recovery codes.
- Email/invitation/recovery: enumeration, token replay, expiry, rate limits,
  параллельное потребление, повторная отправка, истечение/отзыв invitation и
  попытка повысить роль.
- Sessions: отзыв при смене пароля/factor/provider/membership; step-up
  повторно проверяется на защищённых операциях.
- Privacy: токены, коды и PII отсутствуют в логах, traces, метриках и ошибках;
  audit содержит только утверждённый минимум.
- API: contract tests подтверждают единообразие ошибок и отсутствие
  credential/account enumeration.

Провести независимую security review до публичного запуска внешней
аутентификации или восстановления доступа.

## 7. Критерии приёмки

- Для каждой функции есть явная бизнес-потребность и утверждённый threat
  model/assurance policy.
- Каноничная идентичность основана на устойчивом provider subject, а не
  только на email.
- Account linking требует доказательства владения, а recovery не обходит
  tenant/RBAC или MFA-политику.
- Секреты и одноразовые токены не хранятся/логируются в открытом виде.
- Реализованы одноразовость, expiry, rate limit, replay protection и
  отзыв сессий, проверенные автоматизированными тестами.
- Поддержка может диагностировать отказ, восстановить доступ и отключить
  provider по runbook без обходного ослабления авторизации.
- Совместимость с существующими admin credentials и CLI документирована;
  старый flow удаляется только отдельным решением.

## English summary

`PLAN-03` conditionally specifies MFA, OIDC, email verification/invitations,
and local-account recovery. Identity, profile, membership, and session state
must remain separate. Provider subjects—not email alone—identify federated
accounts; account linking, recovery, token storage, rate limits, session
revocation, and support procedures require explicit security decisions before
implementation. No user self-service or identity feature is currently
available.
