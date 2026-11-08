# Pull request

> **Language / Язык:** [English](#english) · [Русский](#russian)
> Fill in the section for your preferred language. Keep both language sections synchronized when changing public documentation.

<a id="english"></a>
## English

### Summary

<!-- What changed, why is the change needed, and which user or operational problem does it address? -->

### Scope and compatibility

- Behaviour/API/schema changes:
- Migration or compatibility impact:
- Security/privacy impact:
- Documentation updated:

### Validation

- [ ] <code>make check</code>
- [ ] <code>make validate-specs</code> (if API/schema changes)
- [ ] <code>make frontend-check</code> and <code>make frontend-build</code> (if frontend changes)
- [ ] <code>docker compose config --quiet</code> (if container configuration changes)
- [ ] Performance/provisioning tests used localhost and a disposable <code>_test</code> database only.

### Review checklist

- [ ] Documentation and configuration reflect the implementation.
- [ ] English documentation appears before Russian and both versions agree.
- [ ] Images, diagrams, anchors and relative links were checked.
- [ ] Public Python modules/classes/functions have meaningful docstrings when added or changed.
- [ ] No secrets, tokens, certificates, production data or credentials are included.
- [ ] Breaking changes, migration requirements and rollback limitations are described.
- [ ] Security invariants and failure behaviour remain deny-by-default.

### Evidence and limitations

<!-- Attach relevant test output or link artifacts. State checks not run and known limitations. -->

---

<a id="russian"></a>
## Русский

### Краткое описание

<!-- Что изменено, зачем это нужно и какую пользовательскую или эксплуатационную проблему решает изменение? -->

### Область и совместимость

- Изменения поведения/API/schema:
- Влияние на миграции и совместимость:
- Влияние на безопасность/privacy:
- Обновлённая документация:

### Проверки

- [ ] <code>make check</code>
- [ ] <code>make validate-specs</code> (при изменении API/schema)
- [ ] <code>make frontend-check</code> и <code>make frontend-build</code> (при изменении frontend)
- [ ] <code>docker compose config --quiet</code> (при изменении container configuration)
- [ ] Performance/provisioning tests выполнялись только на localhost и отдельной БД <code>_test</code>.

### Чек-лист ревью

- [ ] Документация и конфигурация соответствуют реализации.
- [ ] Английская версия документации расположена перед русской, версии совпадают по смыслу.
- [ ] Проверены изображения, схемы, anchors и относительные ссылки.
- [ ] Для новых/изменённых публичных Python-модулей, классов и функций добавлены содержательные docstrings.
- [ ] В изменениях нет секретов, токенов, сертификатов, production-данных и credentials.
- [ ] Описаны breaking changes, миграции и ограничения rollback.
- [ ] Инварианты безопасности и поведение при отказе сохраняют deny-by-default.

### Доказательства и ограничения

<!-- Приложите вывод тестов или ссылки на артефакты. Укажите непроведённые проверки и известные ограничения. -->
