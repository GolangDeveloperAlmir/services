# Changelog

Notable changes to this project are documented here.

## Unreleased

- Add Compose and Dev Container development environments.
- Add reusable CI, pre-commit checks, dependency/security tooling, and
  architectural import tests.
- Generate and validate the OpenAPI specification; document the current
  HTTP-only API in AsyncAPI.
- Add bilingual API, architecture, data-model, operations, and customer
  overview documentation.
- Add local-only Locust scenarios with response-time reports and safety caps.
- Fix duplicate-email conflict detection, including concurrent insert races.
- Complete profile CRUD contracts: stable newest-first pagination, normalized
  email conflicts, explicit not-found responses, and documented admin safety
  invariants; add CRUD service and HTTP regression coverage.
- Add contract-focused Python docstrings to application, migration, tooling,
  and performance modules; synchronize the user-facing and operations guides.

## Не выпущено

- Добавлены Compose и Dev Container для разработки.
- Добавлены переиспользуемый CI, pre-commit, инструменты анализа зависимостей
  и безопасности, а также архитектурные тесты.
- Добавлены генерация и проверка OpenAPI; AsyncAPI описывает текущий HTTP-only API.
- Добавлена двуязычная документация API, архитектуры, данных, эксплуатации и
  обзора для клиентов.
- Добавлены локальные сценарии Locust, временные отчёты и ограничения нагрузки.
- Исправлена обработка конфликтов email, в том числе при конкурентной вставке.
- Уточнены контракты CRUD профилей: стабильная сортировка списка, нормализация
  email, ответы для отсутствующих записей и инварианты защиты администраторов;
  добавлены service- и HTTP-регрессионные тесты.
- Добавлены содержательные docstrings к приложению, миграциям, инструментам и
  нагрузочным сценариям; синхронизированы пользовательские и эксплуатационные
  документы.
