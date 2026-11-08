# PLAN-05: Secure media ingestion and processing

> **Language / Язык:** [English](#english) · [Русский](#russian)
> **Status:** proposed future feature. Upload endpoints and processing workers do not exist; the current catalog is read-only.

<a id="english"></a>
## English

### Goal and security boundary

Design secure ingestion of user-provided images/audio without granting the API container access to the Docker socket, executable content or arbitrary file paths. Every file must be quarantined and processed in a bounded isolated environment. No user-upload feature is available today.

### Scope and terminology

The proposed workflow includes admin-authorized upload intents, quarantined source bytes, a job queue, isolated processing, output verification, publication into a read-only catalog, cleanup and resource quotas.

- **Source:** exact bytes accepted into quarantine; never served directly.
- **Job:** one-time operation with random ID, owner, allowed type and short expiry.
- **Worker:** separate unprivileged process/container, not the API process and not externally reachable.
- **Result:** newly decoded/re-encoded and re-verified output; source bytes are never copied directly into the serving catalog.

Arbitrary archives, SVG/HTML, documents, executables, user scripts, anonymous public uploads, image generation and permanent worker network access are out of scope without separate approval.

### Proposed state machine

~~~mermaid
stateDiagram-v2
    [*] --> created
    created --> receiving
    receiving --> quarantined
    quarantined --> processing
    processing --> published
    processing --> rejected
    created --> expired
    receiving --> rejected
    quarantined --> expired
    processing --> cleanup_failed
    published --> [*]
    rejected --> [*]
    expired --> [*]
~~~

Transitions must be atomic and monotonic. One upload intent cannot be consumed, processed or published more than once.

### Target processing flow

1. An administrator creates a short-lived one-use upload intent with an allowed category, type and size.
2. The receiver enforces actual streamed byte count, request size and rate limits. Content-Length alone is not trusted. Bytes go to a random permission-restricted quarantine directory.
3. Before queueing, validate intent use, quota, file signature and expected type. Reject archives, polyglots and unsupported formats; extension and client MIME are not proof of content type.
4. The queue passes only a job ID and fixed processing profile to the worker.
5. A controller launches a one-job isolated runtime: non-root, read-only root filesystem, dropped capabilities, no-new-privileges, no network, no host PID/IPC, no Docker socket, bounded CPU/RAM/PIDs/time and restricted scratch storage.
6. Decode/re-encode images to a raster allowlist with pixel/frame/dimension/time limits and strip sensitive metadata. Decode audio with duration/channel/sample-rate/size/time constraints. Generate a new output file.
7. Verify output signature, size, hash, category, allowed extension and absence of extra files, then atomically publish.
8. Independent cleanup removes source and scratch files after success, failure or TTL. Reconcile orphan jobs after restarts and alert on cleanup failure.

### Storage, quotas and threats

Quarantine and scratch must be outside the web root and published catalog. Use server-generated paths; never build filesystem paths from user filenames. Restrict per-file size, per-user/admin quota, total storage, queue depth and concurrency. Cleanup must be idempotent and may delete only objects created under the assigned root.

| Threat | Required control |
| --- | --- |
| Path traversal / symlink | Server UUID paths, root-bound file operations and link rejection |
| Oversized file / decompression bomb | Stream byte limits, pixel/frame/duration limits and CPU/RAM/time quotas |
| MIME/extension spoofing | Signature inspection, real decoder and safe re-encoding |
| Decoder exploit | One-job worker without network/capabilities or application secrets |
| Replay/race | One-use intent, atomic state transitions and idempotency |
| Quarantine leakage | Separate volume/network, no serving endpoint and least privilege |
| Disk/queue exhaustion | Quotas, backpressure, TTL and alerting |
| Orphan temporary files | Cleanup on all outcomes, TTL sweeper and reconciliation |
| Copyright abuse | Admin rights confirmation, removal policy and auditable decision |

### API and acceptance criteria

All management endpoints require an active administrator session. An intent is bound to category, type, maximum size, TTL and per-admin/IP limits. Responses must not reveal internal paths, temporary names, stderr or scanner internals. Define API methods/status codes, catalog pagination, deletion, signed URL policy, storage provider, queue, sandbox runtime, moderation responsibility, media profiles and legal process through ADRs before implementation.

Automated and operational tests must prove: unauthenticated/expired/replayed intents cannot accept bytes; streaming limits work with missing or false Content-Length; traversal, symlinks, double extensions, invalid signatures, polyglots, corrupt files and unsupported formats are rejected; worker has no network/socket/host mounts/backend secrets; output is safe and metadata stripped; failures/timeouts/crashes/restarts/disk-full never publish source bytes; cleanup is repeatable and TTL-bounded; concurrent jobs cannot access one another's data; only verified output is served; logs/audit/traces/metrics/URLs contain no source contents, secrets or internal paths.

---

<a id="russian"></a>
## Русский

### Цель и граница безопасности

Спроектировать безопасный приём пользовательских изображений и аудио без доступа API-контейнера к Docker socket, исполняемому содержимому или произвольным файловым путям. Каждый файл должен проходить карантин и обработку в ограниченной изолированной среде. Сейчас функции пользовательской загрузки нет.

### Scope и термины

Предлагаемый процесс включает upload intents с авторизацией администратора, карантин исходных байтов, очередь jobs, изолированную обработку, проверку результата, публикацию в read-only каталог, очистку и ресурсные квоты.

- **Source:** точные байты, принятые в карантин; напрямую клиентам не выдаются.
- **Job:** одноразовая операция со случайным ID, владельцем, разрешённым типом и коротким TTL.
- **Worker:** отдельный непривилегированный процесс/контейнер, не API и недоступный извне.
- **Result:** заново декодированный/перекодированный и повторно проверенный файл; исходные байты не копируются в каталог выдачи.

Произвольные архивы, SVG/HTML, документы, исполняемые файлы, пользовательские скрипты, публичные анонимные загрузки, генерация изображений и постоянный сетевой доступ worker не входят в scope без отдельного решения.

### Предлагаемая машина состояний

~~~mermaid
stateDiagram-v2
    [*] --> created
    created --> receiving
    receiving --> quarantined
    quarantined --> processing
    processing --> published
    processing --> rejected
    created --> expired
    receiving --> rejected
    quarantined --> expired
    processing --> cleanup_failed
    published --> [*]
    rejected --> [*]
    expired --> [*]
~~~

Переходы должны быть атомарными и монотонными. Один upload intent нельзя потребить, обработать или опубликовать повторно.

### Целевой процесс обработки

1. Администратор создаёт короткоживущий одноразовый upload intent с разрешённой категорией, типом и размером.
2. Принимающий endpoint ограничивает фактически прочитанные потоковые байты, размер запроса и rate. Одному Content-Length доверять нельзя. Байты попадают в случайный карантинный каталог с закрытыми правами.
3. До постановки в очередь проверяются одноразовость intent, quota, сигнатура файла и ожидаемый тип. Архивы, polyglot и неподдерживаемые форматы отклоняются; расширение и MIME клиента не доказывают формат.
4. Очередь передаёт worker только job ID и фиксированный processing profile.
5. Контроллер запускает отдельную среду на одну job: non-root, read-only root filesystem, capabilities отключены, no-new-privileges, без сети, host PID/IPC, Docker socket, с лимитами CPU/RAM/PIDs/time и ограниченным scratch storage.
6. Изображения декодируются и перекодируются в raster allowlist с лимитами пикселей/кадров/размеров/времени; чувствительные метаданные удаляются. Audio декодируется с ограничениями длительности, каналов, sample rate, размера и времени. Результат создаётся заново.
7. Проверяются signature, size, hash, category, разрешённое расширение и отсутствие лишних файлов; затем результат атомарно публикуется.
8. Независимая cleanup-задача удаляет source и scratch после успеха, ошибки или TTL. После рестартов сверяются orphan jobs; сбой очистки вызывает alert.

### Хранение, квоты и угрозы

Карантин и scratch должны находиться вне web root и опубликованного каталога. Пути генерирует сервер; нельзя строить их из пользовательских имён файлов. Ограничиваются размер одного файла, quota пользователя/администратора, общий объём, очередь и concurrency. Cleanup должен быть идемпотентным и удалять только объекты под выделенным корнем.

| Угроза | Обязательный контроль |
| --- | --- |
| Path traversal / symlink | Server UUID paths, операции с проверкой корня и запрет ссылок |
| Большой файл / decompression bomb | Поточные лимиты байтов, пикселей/кадров/длительности и CPU/RAM/time quotas |
| Подмена MIME/extension | Проверка сигнатуры, реальный decoder и безопасное перекодирование |
| Эксплойт decoder | Worker на одну job без сети/capabilities и секретов приложения |
| Replay/race | Одноразовый intent, атомарные состояния и idempotency |
| Утечка карантина | Отдельные volume/network, отсутствие endpoint выдачи, least privilege |
| Исчерпание диска/очереди | Quotas, backpressure, TTL и alerting |
| Orphan temporary files | Cleanup при всех исходах, TTL sweeper и reconciliation |
| Copyright abuse | Подтверждение прав администратором, политика удаления и audit-решение |

### API и критерии приёмки

Все endpoints управления требуют активную admin-сессию. Intent связывается с категорией, типом, максимальным размером, TTL и лимитами на администратора/IP. Ответы не должны раскрывать внутренние пути, временные имена, stderr или детали scanner. Методы API/status codes, pagination каталога, удаление, signed URL policy, storage provider, queue, sandbox runtime, модерация, медиа-профили и юридический процесс утверждаются через ADR до реализации.

Автоматические и эксплуатационные тесты должны подтвердить: unauthenticated/expired/replayed intents не принимают байты; streaming limits работают при отсутствующем или ложном Content-Length; traversal, symlink, двойные расширения, invalid signatures, polyglots, повреждённые файлы и неподдерживаемые форматы отклоняются; worker не имеет сети/socket/host mounts/backend secrets; output безопасен, метаданные удалены; failures/timeouts/crashes/restarts/disk-full не публикуют source bytes; cleanup повторяем и ограничен TTL; jobs изолированы друг от друга; выдаются только проверенные результаты; logs/audit/traces/metrics/URLs не содержат содержимого файлов, секретов или внутренних путей.
