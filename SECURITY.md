# Security policy

> **Language / Язык:** [English](#english) · [Русский](#russian)

The implemented controls and operational assumptions are described in the [security architecture guide](docs/security.md). This policy explains how to report a suspected vulnerability responsibly.

<a id="english"></a>
## English

### Reporting a vulnerability

Please do not report security vulnerabilities in public issues, pull requests or discussions. Use GitHub's private vulnerability reporting for this repository: **Security → Advisories → Report a vulnerability**, if enabled. If private reporting is unavailable, contact the repository maintainer privately through an established channel.

Include the affected version/commit, impact, relevant environment details and concise reproduction steps. Do not include real credentials, access tokens, private keys, personal data or production customer data in a report.

### Supported versions

Security fixes are applied to the latest maintained version on the default branch. Upgrade to the latest maintained revision before reporting a suspected fixed issue. The repository does not currently publish a commercial support lifecycle or guaranteed response window.

### Response

The maintainer will acknowledge reports as soon as practical, investigate reproducible reports and coordinate remediation and disclosure with the reporter. Response time depends on availability and severity; no service-level agreement is implied.

### Scope notes

The service is an administrator-only profile API, not a complete identity platform. Security limitations and production prerequisites are documented in [docs/security.md](docs/security.md). Automated checks and badges are not a security certification.

---

<a id="russian"></a>
## Русский

### Сообщение об уязвимости

Не публикуйте сведения об уязвимостях в открытых issues, pull requests или обсуждениях. Используйте приватную форму GitHub для этого репозитория: **Security → Advisories → Report a vulnerability**, если она включена. Если приватная форма недоступна, свяжитесь с сопровождающим проекта конфиденциально через известный канал связи.

Укажите затронутую версию/commit, влияние, важные параметры окружения и краткие шаги воспроизведения. Не включайте в сообщение реальные credentials, access tokens, private keys, персональные или production-данные клиентов.

### Поддерживаемые версии

Исправления безопасности применяются к последней сопровождаемой версии в default branch. Перед сообщением о предположительно исправленной проблеме обновитесь до последней сопровождаемой ревизии. Репозиторий не публикует коммерческий lifecycle поддержки и гарантированный срок ответа.

### Ответ на сообщение

Сопровождающий подтвердит получение сообщения по мере возможности, исследует воспроизводимые отчёты и согласует с автором исправление и раскрытие информации. Срок ответа зависит от доступности сопровождающего и серьёзности проблемы; SLA не подразумевается.

### Границы проекта

Сервис является административным API профилей, а не полноценной Identity-платформой. Ограничения безопасности и production-предпосылки описаны в [docs/security.md](docs/security.md). Автоматические проверки и badges не являются сертификатом безопасности.
