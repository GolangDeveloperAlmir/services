# Media catalog and browser playback / Каталог медиа и воспроизведение

> **Language / Язык:** [English](#english) · [Русский](#russian)

<a id="english"></a>

## Current behavior

The administrator console supports five animated CSS scenes: city, nature,
ocean, beach, and anime-inspired. The scenes are self-contained placeholders,
not bundled photographs or video wallpapers. The motion control pauses the
scene animation. The interface supports Russian and English.

The **Secure API** source reads an operator-managed catalog from the backend.
Both catalog and media responses require an authenticated administrator and
are served from the same HTTPS origin as the console. API media cannot be
selected before sign-in.

The **Local file** source uses a browser file picker. Selected files are held
in the current page as object URLs; the browser does not upload them, and the
application does not store them on the server. Supported local formats are
JPEG, PNG, WebP for images and MP3, OGG, WAV for audio. Each file is limited to
15 MiB. A browser may require a user gesture before audio playback.

The initial catalog is empty because no licensed media is bundled. Operators
must verify usage rights before placing any media in the catalog.

## Operator-managed API catalog

In the repository, files belong in these directories:

```text
media/
  backgrounds/
    city/
    nature/
    ocean/
    beach/
    anime/
  music/
    ambient/
```

In Compose, `./media` is mounted read-only at `/media`. Outside Compose, the
default root is the repository's `media` directory; set `APP_MEDIA_ROOT` only
when intentionally using another trusted, read-only catalog.

The catalog accepts regular files with these extensions:

| Type | Extensions | Per-file limit |
| --- | --- | --- |
| Background image | `.jpg`, `.jpeg`, `.png`, `.webp` | 15 MiB |
| Audio | `.mp3`, `.ogg`, `.wav` | 15 MiB |

Symlinks, unsupported extensions, files outside the fixed category folders,
and files exceeding the limit are excluded. The catalog is capped at 500
eligible files; exceeding that limit makes the catalog unavailable rather
than returning a partial list. The media identifier is an opaque,
path-derived value; API requests never accept a filesystem path. The current
implementation selects response MIME types from the extension. It does not
decode, transcode, malware-scan, or verify the license of operator-provided
files.

After adding or removing curated files, refresh the page or reload the media
source. Do not mount writable user upload directories into the API container.

## Uploads and future processing

There is deliberately no upload endpoint and no file-processing worker in the
current implementation. Local file selection is browser-only. Do not expose
an upload route, mount the Docker socket, or process untrusted files inside
the API container as a shortcut.

The planned quarantine and isolated processing workflow, its limits, cleanup
rules, and acceptance criteria are specified in
[roadmap/05-media-pipeline.md](roadmap/05-media-pipeline.md). That document is
a future specification, not a claim that ingestion or temporary-container
processing is already available.

<a id="russian"></a>
## Текущее поведение

В административной панели доступны пять анимированных CSS-сцен: мегаполис,
природа, океан, пляж и аниме-вдохновлённый вариант. Это автономные визуальные
заглушки, а не включённые в репозиторий фотографии или видеообои. Переключатель
анимации останавливает движение. Интерфейс поддерживает русский и английский.

Источник **«Защищённый API»** читает каталог, управляемый оператором. Доступ к
каталогу и файлам требует действующую сессию администратора; ответы идут с
того же HTTPS origin, что и панель. Выбрать API-медиа до входа нельзя.

Источник **«Локальный файл»** использует системный выбор файла в браузере.
Файл остаётся в текущей странице в виде object URL; браузер не загружает его
на сервер, а приложение не сохраняет его на сервере. Поддерживаются JPEG,
PNG и WebP для изображений, MP3, OGG и WAV для звука; размер каждого файла —
не более 15 MiB. Браузер может потребовать действие пользователя перед
воспроизведением аудио.

Начальный каталог пуст: лицензированные медиафайлы не включены. Перед
добавлением файла оператор обязан проверить права на его использование.

## Каталог API под управлением оператора

Файлы в репозитории размещаются по структуре:

```text
media/
  backgrounds/
    city/
    nature/
    ocean/
    beach/
    anime/
  music/
    ambient/
```

В Compose `./media` монтируется в `/media` только для чтения. При запуске без
Compose корнем по умолчанию является каталог `media` репозитория. Менять
`APP_MEDIA_ROOT` следует только для намеренно выбранного доверенного каталога
только для чтения.

Разрешены только обычные файлы с поддерживаемыми расширениями из таблицы
выше. Символические ссылки, неподдерживаемые форматы, файлы вне
фиксированных категорий и файлы больше 15 MiB исключаются. Каталог ограничен
500 подходящими файлами; при превышении лимита он становится недоступен,
вместо возврата неполного списка. Идентификатор медиа непрозрачен и вычисляется
из пути; API никогда не принимает путь к файловой системе. MIME выбирается
по расширению. Текущая реализация не декодирует, не перекодирует, не проверяет
файлы на вредоносный код и не подтверждает лицензию файлов оператора.

После добавления или удаления файлов обновите страницу или повторно загрузите
источник. Не подключайте к API-контейнеру каталоги загрузок на запись.

## Загрузки и будущая обработка

В текущей реализации намеренно отсутствуют endpoint загрузки и worker
обработки файлов. Выбор локального файла выполняется только браузером. Не
добавляйте endpoint загрузки, не монтируйте Docker socket и не обрабатывайте
недоверенные файлы в API-контейнере в качестве обходного решения.

Будущий процесс карантина и изолированной обработки, ограничения, очистка и
критерии приёмки описаны в
[roadmap/05-media-pipeline.md](roadmap/05-media-pipeline.md). Это будущая
спецификация, а не утверждение о доступности загрузок или временной обработки
в контейнерах сейчас.
